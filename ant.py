import random
import networkx as nx
import graph
import random


class Ant:
    def __init__(self, graph: graph.GraphStruct, source: int, destination: int, alpha: float, beta: float):
        self.graph = graph
        self.source = source
        self.destination = destination
        self.alpha = alpha  # do wywalenia
        self.beta = beta
        self.current = source
        self.road = [source]
        self.visited = [False for i in range(destination + 1)]

    def reached_destination(self):
        if self.current == self.destination: return True
        return False

    def find_next(self):
        unvisited_neighbours = self.get_unvisited_neighbours()
        if len(unvisited_neighbours) == 0: return None
        edge_value_for_ant = []
        sum_ = 0
        probability = []
        for i in unvisited_neighbours:
            new_value = self.graph.get_pheromones(self.current, i) ** self.alpha + self.graph.get_distance(self.current,
                                                                                                           i) ** self.beta
            edge_value_for_ant.append(new_value)
            sum_ += new_value
        for i in edge_value_for_ant:
            probability.append(i / sum_)
        rand = random.random()
        to_pick = list(probability)
        for i in range(1, len(probability)):
            to_pick[i] += to_pick[i - 1]
        to_pick[-1] = 1.0  # to avoid rounding error
        # new=unvisited_neighbours[0]
        new = None
        for i in range(len(probability)):
            if to_pick[i] >= rand:
                new = unvisited_neighbours[i]
        assert new is not None
        return new

    def move_ant(self):
        self.visited[self.current] = True
        next_one = self.find_next()
        if not next_one: return
        self.current = next_one
        self.road.append(self.current)

    def get_unvisited_neighbours(self):
        unvisited_neighbours = []
        for i in self.graph.get_neighbours(self.current):
            if not self.visited[i]:
                unvisited_neighbours.append(i)
        return unvisited_neighbours

    def pheromones(self):
        for i in range(1, len(self.road)):
            new_pher = 1 / self.graph.get_distance(i - 1, i)
            self.graph.deposit_pheromones(i - 1, i, new_pher)
        return

    def find_best(self):
        while not self.reached_destination():
            self.visited[self.current] = True
            unvisited_neighbours = self.get_unvisited_neighbours()
            if len(unvisited_neighbours) == 0: return None
            edge_value_for_ant = []
            sumy = 0
            probability = []
            maxim = 0
            for i in unvisited_neighbours:
                new_value = self.graph.get_pheromones(self.current, i) ** self.alpha + self.graph.get_distance(
                    self.current, i) ** self.beta
                edge_value_for_ant.append(new_value)
                sumy += new_value
            for i in edge_value_for_ant:
                probability.append(i / sumy)
            for i in range(len(probability)):
                if probability[maxim] < probability[i]:
                    maxim = i
            self.current = unvisited_neighbours[maxim]
            self.road.append(self.current)

        return None
