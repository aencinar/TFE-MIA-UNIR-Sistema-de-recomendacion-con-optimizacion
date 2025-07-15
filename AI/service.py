from AI.embeddings import load_embeddings, get_embedding
from AI.clustering import load_cluster_labels, get_cluster_for_embedding
from AI.graph import load_graph_for_cluster, load_neighbors_dict
from AI.load_df import load_csv
from AI.search import search

class RecommendationEngine:
    def __init__(self):
        self.graphs = load_graph_for_cluster()
        self.neighbors_dicts = load_neighbors_dict()
        self.df = load_csv()
        self.labels = load_cluster_labels(self.df)
        self.embeddings = load_embeddings()
        self.code2idx = { code: i for i, code in enumerate((self.df["product_code"].astype(str).str.strip()).tolist()) }

    def recommend(self, input_items, budget, restrictions):
        assert self.embeddings.shape[0] == len(self.df), "El .npy y el CSV deben alinear filas"

        final_path, final_cost, best_weights = search(
            input_items,
            budget=budget,
            restrictions=restrictions,
            df=self.df,
            graphs_by_cluster=self.graphs,
            neighbors_dict=self.neighbors_dicts,
            embeddings=self.embeddings,
            code2idx = self.code2idx
        )

        return {
            "recommended_codes": final_path,
            "total_cost": final_cost,
            "weights": best_weights
        }
