import random
import time
import numpy as np
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity

class AntColony:
    def __init__(
        self,
        graphs_by_cluster,
        df,
        evaluator,
        neighbors_dict,
        alpha=1.0,
        beta=2.0,
        evaporation_rate=0.1,
        pheromone_init=0.1,
        q=1.0
    ):
        self.graphs = {}
        for cluster_id, G in graphs_by_cluster.items():
            if len(G.nodes) > 0 and not isinstance(next(iter(G.nodes)), str):
                mapping = {node: str(node) for node in G.nodes}
                G = nx.relabel_nodes(G, mapping)
            self.graphs[cluster_id] = G

        df = df.copy()
        df['product_code'] = df['product_code'].astype(str).str.strip()
        
        self.df = df
        self.evaluator = evaluator
        self.neighbors_dict = neighbors_dict
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.pheromone_init = pheromone_init
        self.q = q
        self.pheromones = self._initialize_pheromones()
        self.TIME_LIMIT = 0.5
        self.code2row = {str(row['product_code']).strip(): row for _, row in df.iterrows()}
        
        self.code_to_cluster = {
            str(code).strip(): cluster 
            for code, cluster in zip(df['product_code'], df['cluster'])
        }
        self.code_to_data = {
            str(row['product_code']).strip(): {
                'price': row['price'],
                'allergens': row['allergens'],
                'embedding': row['embedding']
            } for _, row in df.iterrows()
        }
        self.valid_codes = set(df['product_code'])

    def _initialize_pheromones(self):
        pheromones = {}
        for cluster_id, G in self.graphs.items():
            for u, v in G.edges():
                pheromones[(cluster_id, u, v)] = self.pheromone_init
                pheromones[(cluster_id, v, u)] = self.pheromone_init
        return pheromones
        
    def _heuristic(self, current_node, candidate_nodes, G):

        emb_curr = G.nodes[current_node]["embedding"].reshape(1, -1)
        embs = np.array([G.nodes[n]["embedding"] for n in candidate_nodes])
        prices = np.array([G.nodes[n]["price"] for n in candidate_nodes])

        epsilon = 1e-5
        price_scores = 1.0 / (prices + epsilon)
        sem_sims = cosine_similarity(emb_curr, embs)[0]
        heuristics = price_scores * sem_sims + epsilon
        return heuristics


    def build_solution(self,
        products_list, restrictions=None, budget=None, k_neighbors=10
    ):
        path = []
        total_cost = 0.0
        df = self.df.copy()

        for orig in products_list:
            orig_str = str(orig).strip()
            if orig_str not in self.code2row:
                path.append(orig_str)
                continue

            cluster = self.code2row[orig_str]['cluster']
            candidates_df = df[df['cluster'] == cluster].copy()
            if len(candidates_df) == 0:
                path.append(orig_str)
                continue

            emb_o = np.array(self.code2row[orig_str]['embedding']).reshape(1, -1)
            emb_matrix = np.stack(candidates_df['embedding'].values)
            sims = cosine_similarity(emb_o, emb_matrix)[0]

            # Top-k más similares (incluye el original)
            candidates_df['sim'] = sims
            candidates_df = candidates_df.sort_values('sim', ascending=False)
            top_candidates = candidates_df.head(k_neighbors+1)  # +1 para asegurar incluir el original

            if restrictions:
                def cumple_alergenos(row):
                    return all(r == 0 or row['allergens'][i] == 0 for i, r in enumerate(restrictions))
                top_candidates = top_candidates[top_candidates.apply(cumple_alergenos, axis=1)]

            if budget is not None:
                top_candidates = top_candidates[top_candidates['price'] + total_cost <= budget]

            top_candidates = top_candidates.sort_values('price')
            best = None
            for _, row in top_candidates.iterrows():
                if row['product_code'] != orig_str:
                    best = row
                    break

            if best is not None:
                path.append(best['product_code'])
                total_cost += float(best['price'])
            else:
                path.append(orig_str)
                total_cost += float(self.code2row[orig_str]['price'])

        return path, total_cost


    def _evaporate_pheromones(self):
        for key in list(self.pheromones.keys()):
            self.pheromones[key] *= (1 - self.evaporation_rate)

    def _update_pheromones(self, best_solution, best_score):
        if best_solution is None:
            return
        delta = self.q / (best_score + 1e-5)
        for i in range(len(best_solution) - 1):
            u = best_solution[i]
            v = best_solution[i + 1]
            if u not in self.df['product_code'].values:
                continue
                
            try:
                cluster_id = self.df.loc[self.df['product_code'] == u, "cluster"].iloc[0]
                key = (cluster_id, u, v)
                if key in self.pheromones:
                    self.pheromones[key] += delta
            except Exception as e:
                print(f"⚠️ Error actualizando feromonas: {str(e)[:50]}")

    def run(
        self,
        shopping_list_ids,
        budget,
        restrictions=None,
        n_ants=3,
        n_iterations=3,
        timeout: float = 0.5
    ):
        best_global_solution = None
        best_global_score = float("inf")
        global_start = time.time()

        for iteration in range(n_iterations):
            iter_start = time.time()
            
            if time.time() - global_start > timeout:
                break

            best_iter_solution = None
            best_iter_score = float("inf")

            for ant in range(n_ants):
                ant_start = time.time()
                if time.time() - global_start > timeout:
                    break
                    
                path, cost = self.build_solution(
                    shopping_list_ids,
                    budget=budget, 
                    restrictions=restrictions
                )
                
                if path is None or time.time() - global_start > timeout:
                    continue

                if any(str(code).strip() not in self.valid_codes for code in path):
                    continue
                    
                score = self.evaluator.evaluate(path, shopping_list_ids, restrictions)
                
                print(f"Hormiga {ant+1}/{n_ants} | T: {time.time()-ant_start:.3f}s | Costo: {cost:.2f}/{budget} | Score: {score:.2f}")
                
                if score < best_iter_score:
                    best_iter_solution = path
                    best_iter_score = score
                    
                if score < best_global_score:
                    best_global_solution = path
                    best_global_score = score

            if best_iter_solution is not None:
                print(f"🔥 Actualizando feromonas con score: {best_iter_score:.2f}")
                self._evaporate_pheromones()
                self._update_pheromones(best_iter_solution, best_iter_score)

        if best_global_solution is None:
            return None, float("inf")
        
        print(f"🏆 Mejor solución global: {best_global_score:.2f} | Tiempo total: {time.time()-global_start:.3f}s")
        return best_global_solution, best_global_score