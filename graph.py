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
        self.graph[u][v]["pheromones"] += (1 - self.evaporation_rate) + how_much

    def get_distance(self, u, v): return self.graph[u][v]["distance"]

    def get_neighbours(self, u): return list(self.graph[u].keys())

    def draw_graph(self, shortest_path):
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
        edge_labels = nx.get_edge_attributes(self.graph, "pheromones")
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels)

        ax = plt.gca()
        ax.margins(0.08)
        plt.axis("off")
        plt.tight_layout()
        plt.show()
