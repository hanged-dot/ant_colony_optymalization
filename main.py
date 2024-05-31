import json

from aco import ACO
import networkx as nx
import load_graph
import fire
import matplotlib.pyplot as plt
import result_gui

def default_graph(pheromones=1, distance=1):
    n=5
    G = nx.Graph()
    nodes = [i for i in range(n)]
    G.add_nodes_from(nodes)
    for i in range(n - 1):
        for j in range(i + 1, n):
            G.add_edge(i, j, pheromones=pheromones, distance=distance)
    return G


def get_graph(pheromones, filename=None):
    if filename is None:
        return default_graph()
    else:
        E = load_graph.load_graph(f"graphs/{filename}")
        G = nx.Graph()
        for u, v, dist in E:
            G.add_edge(u-1, v-1, distance=dist, pheromones=pheromones)
        return G

def get_config(filename=None):
    if filename is None:
        return {
                "ants": 10,
                "days": 50,
                "pheromones": 0.2,
                "evaporation": 0.1,
                "importance_of_pheromones": 1,
                "importance_of_distance": 1
            }
    else:
        with open(f"configs/{filename}", 'r') as f:
            data = json.load(f)
        return data

def main(graph=None, config=None, out="results/ant_data.json", draw_graph=True, draw_plot=True):
    config_dict = get_config(config)
    G = get_graph(config_dict["pheromones"], graph)
    n = len(G.nodes)

    aco = ACO(
        G,
        n,
        config_dict["ants"],
        config_dict["pheromones"],
        config_dict["evaporation"],
        config_dict["importance_of_pheromones"],
        config_dict["importance_of_distance"],
        config_dict["days"],
    )

    path, results = aco.find_path()

    dijkstra_path = nx.dijkstra_path(G, 0, n - 1, "distance")
    dijkstra_cost = nx.path_weight(G, dijkstra_path, "distance")

    data = {
        "best_path": dijkstra_cost,
        "ant_optimization": [],
    }
    for i, cost in enumerate(results):
        data["ant_optimization"].append({
            "day": i+1,
            "path_cost": cost,
        })

    with open(out, 'w') as f:
        json.dump(data, f, indent=4)

    if draw_graph:
        aco.graph.draw_graph(path, "drawing/graph.png")

    if draw_plot:
        days = [entry["day"] for entry in data["ant_optimization"]]
        paths = [entry["path_cost"] for entry in data["ant_optimization"]]

        plt.plot(days, paths, marker='.', linestyle='-')
        plt.xlabel('Day')
        plt.ylabel('Path')
        plt.axhline(y=dijkstra_cost, color='r', linestyle='--', label='Dijkstra')
        plt.title('Path vs Day')
        plt.grid(True)
        plt.savefig("drawing/plot.png")
        plt.show()

    if draw_plot and draw_graph:
        result_gui.resultwindow("drawing/graph.png","drawing/plot.png")




if __name__ == '__main__':
    fire.Fire(main)
