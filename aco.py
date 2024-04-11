import random
import networkx as nx
import matplotlib.pyplot as plt
from ant import Ant
import networkx as nx
from graph import GraphStruct


class ACO:
    def __init__(self, graph: nx.DiGraph, nodes: int, ants: int, pheromone_per_ant: float,
                 evaporation_rate: float, alpha_pheromones: float, beta_pheromones: float, days: int):
        self.graph_base: nx.DiGraph = graph
        self.nodes = nodes
        self.ants = ants
        self.pheromone_per_ant = pheromone_per_ant
        self.evaporation_rate = evaporation_rate
        self.alpha_pheromones = alpha_pheromones
        self.beta_pheromones = beta_pheromones
        self.days = days
        self.ant_array = []
        # Initialize all edges of the graph with a pheromone value of 1.0
    def __post_init__(self):
        self.graph=GraphStruct(self.graph_base, self.evaporation_rate)
        for e in self.graph.edges:
            self.graph.set_pheromones(e[0],e[1],1.0)

    def ant_path_pheromone_deposit(self):
        for a in self.ant_array:
            if a.reached_destination():
                a.pheromones()

    def find_path(self):
        for i in range(self.days):
            self.ant_array.clear()
            for _ in range(self.ants):
                new_ant = Ant(self.graph, 0, self.nodes - 1,self.alpha_pheromones,self.beta_pheromones)
                self.ant_array.append(new_ant)
            for a in self.ant_array:
                while not a.reached_destination() or a.get_unvisited_neighbours(a.current) != []:
                    a.move()
            self.ant_path_pheromone_deposit()

        short_path= self.find_solution()
        self.graph.draw_graph(short_path)
    def find_solution(self):
        new_ant = Ant(self.graph, 0, self.nodes - 1, self.alpha_pheromones, self.beta_pheromones)
        new_ant.find_best()
        short_path=[]
        for i in range(1,len(new_ant.road)):
            short_path.append((new_ant.road[i-1],new_ant.road[i]))
        return short_path



