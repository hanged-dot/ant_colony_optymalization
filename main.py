from aco import ACO
import networkx as nx

G = nx.Graph()
n = 8  # number of nodes start on 0 end on n-1
ants = 5
days = 10
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
        G.add_edge(i, j, pheromones=pheromones, distance=distance)

dijkstra_path = nx.dijkstra_path(G, 0, n-1)
dijkstra_cost = nx.path_weight(G, dijkstra_path, "distance")

print(f"Dijkstra - path: {dijkstra_path}, cost: {dijkstra_cost}")

aco = ACO(G, n, ants, pheromones, evaporation, importance_of_pheromones, importance_of_distance, days)

aco.find_path()
