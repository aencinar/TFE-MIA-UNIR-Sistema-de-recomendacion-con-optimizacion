from sklearn.metrics.pairwise import cosine_distances
import numpy as np
    

class MultiObjectiveEvaluator:
    def __init__(self, df, weights, budget=None):
        self.df = df
        self.weights = np.asarray(weights, dtype=float)
        self.budget = budget
        self.valid_codes = set(df['product_code'].astype(str).str.strip())
        self.code2row = {
            str(row['product_code']).strip(): row
            for _, row in self.df.iterrows()
        }
        
    def set_weights(self, new_weights):
        self.weights = np.asarray(new_weights, dtype=float)
    
    def set_budget(self, budget):
        self.budget = budget

    def evaluate(self, path, original_ids, restrictions=None):
        w_price, w_penalty, w_dist = self.weights
        total_price = 0.0
        total_penalty = 0.0
        total_dist = 0.0

        for orig, sub in zip(original_ids, path):
            orig_str = str(orig).strip()
            sub_str = str(sub).strip()
            
            if orig_str not in self.valid_codes or sub_str not in self.valid_codes:
                return 1e9

            try:
                prod_o = self.code2row[orig_str]
                prod_s = self.code2row[sub_str]
            except IndexError:
                return 1e9

            total_price += float(prod_s["price"])

            if restrictions:
                for i, want_free in enumerate(restrictions):
                    if want_free == 1 and prod_s["allergens"][i] == 1:
                        total_penalty += 1

            emb_o = prod_o["embedding"].reshape(1, -1)
            emb_s = prod_s["embedding"].reshape(1, -1)
            total_dist += cosine_distances(emb_o, emb_s)[0, 0]
            
        if self.budget and total_price > self.budget:
            over = total_price - self.budget
            total_price += 10 * over

        score = w_price * total_price + w_penalty * total_penalty + w_dist * total_dist
        print(f"📊 Evaluación: Precio={total_price:.2f} | Penalty={total_penalty} | Dist={total_dist:.2f} | Score={score:.2f}")
        return score