import random
import networkx as nx
import matplotlib.pyplot as plt
from ant import Ant
import networkx as nx
from typing import Optional


INITIAL_PHEROMONE = 1.0


class ACO:
    def __init__(self, graph: nx.Graph, nodes_count: int, ants: int, pheromone_per_ant: float,
                 evaporation_rate: float, alpha_pheromones: float, beta_pheromones: float, days: int,src: int = 0, trg: Optional[int] = None):
        self.graph: nx.Graph = graph
        self.nodes_count = nodes_count
        self.ants_count = ants
        self.pheromone_per_ant = pheromone_per_ant
        self.evaporation_rate = evaporation_rate
        self.alpha_pheromones = alpha_pheromones
        self.beta_pheromones = beta_pheromones
        self.days = days
        self.ant_array = []
        self.src = src
        self.trg = trg or nodes_count - 1

    def ant_path_pheromone_deposit(self):
        for a in self.ant_array:
            a.pheromones()

    def run(self):
        shortest_ever = ([], float('inf'))
        results = []
        for i in range(self.days):
            self.ant_array.clear()
            for _ in range(self.ants_count):
                self.ant_array.append(Ant(self.graph,self.nodes_count, self.src,self.trg , self.alpha_pheromones, self.beta_pheromones, self.pheromone_per_ant))
            for a in self.ant_array: a.move_ant()
            self.ant_path_pheromone_deposit()
            ant_roads = [list(zip(ant.road,ant.road[1:])) for ant in self.ant_array]
            paths=[(ant_r,self.path_total_dist(ant_r)) for ant_r in ant_roads]
            shortest_path = min(paths, key=lambda x: x[1])
            if shortest_path[1] < shortest_ever[1]:
                shortest_ever = shortest_path
            results.append(shortest_path[1])
            self.evaporate()
        return shortest_ever, results

    def path_total_dist(self, path):
        length = 0
        for u, v in path:
            length += self.graph[u][v]["distance"]
        return length

    def find_solution(self):
        new_ant = Ant(self.graph, self.nodes_count,self.src, self.trg, self.alpha_pheromones, self.beta_pheromones, self.pheromone_per_ant)
        road = new_ant.solve(new_ant.src,new_ant.destination,set())
        return list(reversed(road))

    def find_path(self):
        shortest_ever, results = self.run()
        final_path = self.find_solution()
        final_path = list(zip(final_path,final_path[1:]))
        return (final_path, self.path_total_dist(final_path)), results

    def evaporate(self):
        for u,v in self.graph.edges():
            self.graph[u][v]["pheromones"] = (1 - self.evaporation_rate) * self.graph[u][v]["pheromones"]

    def draw_graph(self, shortest_path, dijkstra_nodes, directory):
        plt.figure()
        for e in self.graph.edges():
            source, destination = e[0], e[1]
            self.graph[source][destination]["pheromones"] = round(self.graph[source][destination]["pheromones"])
        result_graph = nx.Graph
        #nx.draw(self.graph, pos, width=4)
        nodes_of_shortest=[a for a,_ in shortest_path]
        nodes_of_shortest.append(shortest_path[-1][1])
        dijkstra_path= list(zip(dijkstra_nodes,dijkstra_nodes[1:]))
        pos = nx.spring_layout(self.graph, seed=2)
        nx.draw_networkx_nodes(self.graph, pos, nodelist=nodes_of_shortest, node_size=300)
        nx.draw_networkx_nodes(self.graph, pos, nodelist=dijkstra_nodes, node_size=300)
        nx.draw_networkx_labels(self.graph, pos, font_size=10)
        nx.draw_networkx_edges(self.graph,pos,edgelist=list(shortest_path),edge_color="blue",width=4)
        nx.draw_networkx_edges(self.graph, pos, edgelist=list(dijkstra_path), edge_color="red", width=4, style="dashed")


        # node labels

        # edge cost labels
        #edge_pheromones = nx.get_edge_attributes(self.graph, "pheromones")
        #nx.draw_networkx_edge_labels(self.graph, pos, edge_pheromones, label_pos=0.3, font_color='blue')
        #edge_distance = nx.get_edge_attributes(self.graph, "distance")
        #nx.draw_networkx_edge_labels(self.graph, pos, edge_distance, label_pos=0.7, font_color='green')

        ax = plt.gca()
        ax.margins(0.08)
        plt.axis("off")
        # plt.tight_layout()
        plt.savefig(directory)
        # plt.show()