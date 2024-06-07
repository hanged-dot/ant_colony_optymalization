import networkx as nx
import random
import sys
sys.setrecursionlimit(10_000)



class Ant:
    def __init__(self, graph: nx.Graph, nodes_count: int, source: int, destination: int, alpha: float, beta: float, pheromone: float):
        self.graph = graph
        self.source = source
        self.destination = destination
        self.alpha = alpha
        self.beta = beta
        self.src = source
        self.dst = destination
        self.pheromone = pheromone
        self.road = [source]
        self.visited = [False for i in range(nodes_count + 1)]

    def move(self, node, destination, visited):
        visited.add(node)
        if node == destination:
            return [node]
        v = self.find_next(node,visited)
        while v:
            result = self.move(v, destination, visited)
            if result:
                result.append(node)
                return result
            v = self.find_next(node, visited)
        return None

    def solve(self, node, destination, visited):
        visited.add(node)
        if node == destination:
            return [node]
        v = self.find_best(node,visited)
        while v:
            result = self.move(v, destination, visited)
            if result:
                result.append(node)
                return result
            v = self.find_best(node, visited)
        return None

    def find_next(self,node,visited):
        unvisited_neighbours = [v for v in self.graph[node] if v not in visited]
        if len(unvisited_neighbours) == 0: return None
        edge_value_for_ant = []
        sum_ = 0
        probability = []
        for i in unvisited_neighbours:
            new_value = self.graph[node][i]["pheromones"] ** self.alpha * (1 / self.graph[node][i]["distance"]) ** self.beta
            edge_value_for_ant.append(new_value)
            sum_ += new_value
        for i in edge_value_for_ant:
            probability.append(i / sum_)
        rand = random.random()
        to_pick = list(probability)
        for i in range(1, len(probability)):
            to_pick[i] += to_pick[i - 1]
        to_pick[-1] = 1.0
        new = 0
        for i in range(len(probability)):
            if to_pick[i] >= rand:
                new = unvisited_neighbours[i]
                break
        return new

    def move_ant(self):
        self.road = self.move(self.src, self.dst, set())

    def pheromones(self):
        for i in range(1, len(self.road)):
            new_pheromone = (1 / self.graph[self.road[i - 1]][self.road[i]]["distance"]) * self.pheromone
            self.graph[self.road[i - 1]][self.road[i]]["pheromones"] +=new_pheromone
        return

    def find_best(self, node, visited):
            unvisited_neighbours = [v for v in self.graph[node] if v not in visited]
            if len(unvisited_neighbours) == 0: return None
            edge_value_for_ant = []
            sumy = 0
            probability = []
            maxim = 0
            for i in unvisited_neighbours:
                new_value = self.graph[node][i]["pheromones"] ** self.alpha * (1 / self.graph[node][i]["distance"]) ** self.beta
                edge_value_for_ant.append(new_value)
                sumy += new_value
            for i in edge_value_for_ant:
                probability.append(i / sumy)
            for i in range(len(probability)):
                if probability[maxim] < probability[i]:
                    maxim = i
            return unvisited_neighbours[maxim]

