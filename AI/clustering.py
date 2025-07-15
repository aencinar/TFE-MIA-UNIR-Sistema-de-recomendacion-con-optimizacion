import numpy as np

def load_cluster_labels(df):
    return dict(zip(df["product_code"], df["cluster"]))

def get_cluster_for_embedding(idx, labels):
    return labels[idx]
