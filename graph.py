from dataclasses import dataclass
from typing import List
import networkx as nx
import matplotlib.pyplot as plt


class GraphStruct:
    def __init__(self, graph: nx.Graph, evaporation_rate: float):
        self.graph = graph
        self.evaporation_rate = evaporation_rate

    # initialize graph pheromones(not needed for now)
    def set_pheromones(self, u, v, how_much): self.graph[u][v]["pheromones"] = how_much

    def get_pheromones(self, u, v): return self.graph[u][v]["pheromones"]

    def deposit_pheromones(self, u, v, how_much):
        self.graph[u][v]["pheromones"] += how_much

    def get_distance(self, u, v): return self.graph[u][v]["distance"]

    def evaporate(self):
        for e in self.graph.edges():
            u, v = e[0], e[1]
            self.graph[u][v]["pheromones"] = (1 - self.evaporation_rate) * self.graph[u][v]["pheromones"]

    def get_neighbours(self, u): return list(self.graph[u].keys())

    def draw_graph(self, shortest_path, directory):
        for e in self.graph.edges():
            source, destination = e[0], e[1]
            self.graph[source][destination]["pheromones"] = round(self.graph[source][destination]["pheromones"])
        pos = nx.spring_layout(self.graph, seed=2)
        nx.draw(self.graph, pos, width=4)

        nx.draw_networkx_nodes(self.graph, pos, node_size=700)

        # nx.draw_networkx_edges(G, pos, width=2)
        nx.draw_networkx_edges(
            self.graph,
            pos,
            edgelist=list(shortest_path),
            edge_color="r",
            width=4,
        )

        # node labels
        nx.draw_networkx_labels(self.graph, pos, font_size=20)
        # edge cost labels
        edge_pheromones = nx.get_edge_attributes(self.graph, "pheromones")
        nx.draw_networkx_edge_labels(self.graph, pos, edge_pheromones, label_pos=0.3, font_color='blue')
        edge_distance = nx.get_edge_attributes(self.graph, "distance")
        nx.draw_networkx_edge_labels(self.graph, pos, edge_distance, label_pos=0.7, font_color='green')

        ax = plt.gca()
        ax.margins(0.08)
        plt.axis("off")
        #plt.tight_layout()
        plt.savefig(directory)
        plt.show()
