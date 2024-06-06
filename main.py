import json

from ant_colony import AntColony
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

    # aco = ACO(
    #     G,
    #     n,
    #     config_dict["ants"],
    #     config_dict["pheromones"],
    #     config_dict["evaporation"],
    #     config_dict["importance_of_pheromones"],
    #     config_dict["importance_of_distance"],
    #     config_dict["days"],
    # )

    aco = AntColony(
        G,
        n,
        config_dict["ants"],
        config_dict["pheromones"],
        config_dict["evaporation"],
        config_dict["importance_of_pheromones"],
        config_dict["importance_of_distance"],
        config_dict["days"],
    )

    path_and_dist, results = aco.find_path()
    path, dist = path_and_dist

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
        plot_graph(G, path, "drawing/graph.png")

    if draw_plot:
        days = [entry["day"] for entry in data["ant_optimization"]]
        paths = [entry["path_cost"] for entry in data["ant_optimization"]]
        plt.figure()
        plt.plot(days, paths, marker='.', linestyle='-')
        plt.xlabel('Day')
        plt.ylabel('Path')
        plt.axhline(y=dijkstra_cost, color='r', linestyle='--', label='Dijkstra')
        plt.title('Path vs Day')
        plt.grid(True)
        plt.savefig("drawing/plot.png")
        # plt.show()
    # if draw_plot and draw_graph:
        return result_gui.resultwindow("drawing/graph.png","drawing/plot.png")

def plot_graph(graph, shortest_path, directory):
    plt.figure()
    for e in graph.edges():
        source, destination = e[0], e[1]
        graph[source][destination]["pheromones"] = round(graph[source][destination]["pheromones"])
    pos = nx.spring_layout(graph, seed=2)
    nx.draw(graph, pos, width=4)

    nx.draw_networkx_nodes(graph, pos, node_size=700)

    # nx.draw_networkx_edges(G, pos, width=2)
    nx.draw_networkx_edges(
        graph,
        pos,
        edgelist=list(shortest_path),
        edge_color="r",
        width=4,
    )

    # node labels
    nx.draw_networkx_labels(graph, pos, font_size=20)
    # edge cost labels
    edge_pheromones = nx.get_edge_attributes(graph, "pheromones")
    nx.draw_networkx_edge_labels(graph, pos, edge_pheromones, label_pos=0.3, font_color='blue')
    edge_distance = nx.get_edge_attributes(graph, "distance")
    nx.draw_networkx_edge_labels(graph, pos, edge_distance, label_pos=0.7, font_color='green')

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    #plt.tight_layout()
    plt.savefig(directory)
    # plt.show()


if __name__ == '__main__':
    fire.Fire(main)
