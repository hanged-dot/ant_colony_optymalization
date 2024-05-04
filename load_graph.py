def load_graph(name):
    edges = []
    with open(name, "r") as f:
        lines = f.readlines()
        for l in lines:
            s = l.split()
            if (s[0] == "e"):
                (a, b, c) = (int(s[1]), int(s[2]), int(s[3]))
                edges.append((a, b, c))

    return edges
