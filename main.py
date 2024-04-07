from aco import ACO
import networkx as nx

G = nx.Graph()
n = 5  # number of nodes start on 0 end on n-1
ants = 3
days = 100
pheromones = 0.2
distance = 1
evaporation = 0.1
importance_of_pheromones = 1
importance_of_distance = 1

nodes = [i for i in range(n)]
G.add_nodes_from(nodes)
edges = []
for i in range(n - 1):
    for j in range(i + 1, n):
        edges.append((i, j))
G.add_edges_from(edges, color='red', pheromones=pheromones, distance=distance)

aco = ACO(G, n, ants, pheromones, evaporation, importance_of_pheromones, importance_of_distance, days)

#aco.find_path()
aco.draw_graph()
