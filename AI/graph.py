import pickle

def load_graph_for_cluster():
    path = "AI/graphs.pkl"
    with open(path, "rb") as f:
        G = pickle.load(f)
    return G


def load_neighbors_dict():
    with open('AI/neighbors_dict.pkl', 'rb') as f:
        neighbors_dict = pickle.load(f)

    return neighbors_dict
