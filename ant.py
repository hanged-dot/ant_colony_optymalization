import random
import networkx as nx
class Ant:
    def __init__(self, graph: nx.Graph, source: int, destination: int):
        self.graph = graph
        self.source = source
        self.destination = destination
        self.current = source
        self.road = []
        self.visited = [False for i in range(destination+1)]

    def reached_destination(self):
        if self.current == self.destination: return True
        return False

    def find_next(self):
        new = 0

        # add implementation
        return new

    def move(self):
        self.road.append(self.current)
        self.visited[self.current] = True
        self.current = self.find_next()

    def get_unvisited(self):
        neighbours = []
        for i in range(len(self.visited)):
            if not self.visited[i]:
                neighbours.append(i)
        return neighbours
    def get_neighbours(self):
        neighbours = []
        return neighbours
