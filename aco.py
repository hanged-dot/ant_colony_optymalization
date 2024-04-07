import random
import networkx as nx
import matplotlib.pyplot as plt
from ant import Ant


class ACO:
    def __init__(self, graph: nx.Graph, nodes: int, ants: int, pheromone_per_ant: float,
                 evaporation_rate: float, alpha_pheromones: float, beta_distance: float, days: int):
        self.graph = graph
        self.nodes = nodes
        self.ants = ants
        self.pheromone_per_ant = pheromone_per_ant
        self.evaporation_rate = evaporation_rate
        self.alpha_pheromones = alpha_pheromones
        self.beta_distance = beta_distance
        self.days = days
        self.ant_array = []
        # Initialize all edges of the graph with a pheromone value of 1.0


    def find_path(self):
        for i in range(self.days):
            self.ant_array.clear()
            for _ in range(self.ants):
                new_ant = Ant(self.graph, 0, self.nodes - 1)
                self.ant_array.append(new_ant)
            for a in self.ant_array:
                while not a.reached_destination() or a.get_neighbours() != []:
                    a.move()

    def draw_graph(self):
        nx.draw(self.graph, with_labels=True, font_weight='bold')
        #nx.draw_networkx_edge_labels(self.graph)
        plt.show()
