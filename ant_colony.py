import random
from typing import Optional

import networkx as nx
import sys

INITIAL_PHEROMONE = 1.0

DISTANCE = "distance"
PHEROMONES = "pheromones"
sys.setrecursionlimit(10_000)

class AntColony:
    def __init__(self, graph: nx.Graph, nodes_count: int, ants: int, pheromone_per_ant: float,
                 evaporation_rate: float, alpha_pheromones: float, beta_pheromones: float, days: int,
                 src: int = 0, trg: Optional[int] = None):
        self.graph = graph
        self.n_nodes = nodes_count
        self.n_ants = ants
        self.pheromone_per_ant = pheromone_per_ant
        self.evaporation_rate = evaporation_rate
        self.alpha_pheromones = alpha_pheromones
        self.beta_pheromones = beta_pheromones
        self.days = days
        self.ant_array = []

        self.src = src
        self.trg = trg or self.n_nodes - 1
        # Initialize all edges of the graph with a pheromone value of INITIAL PHEROMONE

    def _gen_many_paths(self):
        paths = [self._gen_path() for _ in range(self.n_ants)]
        return [(path, self.calc_dist(path)) for path in paths]

    def _gen_path(self):
        path = self._gen_path_dfs(self.src, self.trg, set())
        nodes_in_path = list(reversed(path))
        zipped = zip(nodes_in_path, nodes_in_path[1:])
        return list(zipped)


    def calc_dist(self, path):
            total_dist = 0
            for u, v in path:
                total_dist += self.graph[u][v][DISTANCE]
            return total_dist

    def _gen_path_dfs(self, node: int, trg: int, visited: set[int]):
        visited.add(node)
        if node == trg:
            return [node]

        v = self._probability_based_move(node, visited)
        while v:
            result = self._gen_path_dfs(v, trg, visited)
            if result:
                result.append(node)
                return result
            v = self._probability_based_move(node, visited)
        return None

    def _probability_based_move(self, node, visited):
        neighbours = [v for v in self.graph[node] if v not in visited]
        weights = [self._edge_weight(node, v) for v in neighbours]
        if not neighbours:
            return None
        return random.choices(neighbours, weights)[0]

    def _best_move(self, node, visited):
        neighbours = [v for v in self.graph[node] if v not in visited]
        weights = [self._edge_weight(node, v) for v in neighbours]
        w = max(weights)
        i = weights.index(w)
        return neighbours[i]

    def _final_path_dfs(self, node: int, trg: int, visited: set[int]):
        # breakpoint()
        visited.add(node)
        if node == trg:
            return [node]

        v = self._best_move(node, visited)
        while v:
            result = self._gen_path_dfs(v, trg, visited)
            if result:
                result.append(node)
                return result
            v = self._best_move(node, visited)
        return None

    def _edge_weight(self, u: int, v: int):
        return (self.graph[u][v][PHEROMONES] ** self.alpha_pheromones *
                (1 / self.graph[u][v][DISTANCE]) ** self.beta_pheromones)

    def _deposit_pheromone(self, paths):
        for path in paths:
            for u, v in path:
                self.graph[u][v][PHEROMONES] += self.pheromone_per_ant

    def _evaporate_pheromones(self):
        for u, v in self.graph.edges:
            self.graph[u][v][PHEROMONES] -= self.graph[u][v][PHEROMONES] * self.evaporation_rate

    def run(self):
        shortest_path = None
        shortest_ever = ([], float('inf'))
        shortest_path_each_day = []
        for i in range(self.days):
            paths_with_dist = self._gen_many_paths()
            self._deposit_pheromone(
                map(lambda t: t[0], paths_with_dist)
            )
            shortest_path = min(paths_with_dist, key=lambda x: x[1])
            print(shortest_path)
            if shortest_path[1] < shortest_ever[1]:
                shortest_ever = shortest_path
            shortest_path_each_day.append(shortest_path[1])
            self._evaporate_pheromones()
        return shortest_ever, shortest_path_each_day

    def final_path(self):
        path = self._final_path_dfs(self.src, self.trg, set())
        nodes_in_path = list(reversed(path))
        zipped = zip(nodes_in_path, nodes_in_path[1:])
        return list(zipped)

    def find_path(self):
        shortest, results = self.run()
        final_path = self.final_path()
        return (final_path, self.calc_dist(final_path)), results