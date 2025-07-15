import numpy as np
import random

class GeneticOptimizer:
    def __init__(
        self,
        df,
        fast_aco,
        shopping_list_ids,
        budget,
        restrictions,
        population_size=20,
        generations=15,
        mutation_rate=0.1,
        elitism=1
    ):
        self.aco = fast_aco
        self.df = df
        self.shopping_list_ids = shopping_list_ids
        self.budget = budget
        self.restrictions = restrictions
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.elitism = elitism
        self.fitness_cache = {}
        self.valid_codes = set(self.df['product_code'])

    def _init_population(self):
        pop = []
        for _ in range(self.population_size):
            weights = np.random.dirichlet(np.ones(3))
            pop.append(weights.tolist())
        return pop

    def _evaluate_fitness(self, weights):
        key = tuple(round(w, 4) for w in weights)
        if key in self.fitness_cache:
            return self.fitness_cache[key]

        # normaliza y aplica
        norm_w = np.asarray(weights, dtype=float)
        norm_w = norm_w / norm_w.sum() if norm_w.sum() else np.ones_like(norm_w)/3
        self.aco.evaluator.set_weights(norm_w)

        # ejecuta ACO de forma ligera
        path, cost = self.aco.run(
            self.shopping_list_ids, self.budget, self.restrictions,
            n_ants=5, 
            n_iterations=5,  # Aumentar exploración
            timeout=0.5
        )

        # fitness:
        if path is None:
            try:
                # Obtener precios de productos ORIGINALES
                original_prices = []
                for code in self.shopping_list_ids:
                    str_code = str(code).strip()
                    if str_code in self.valid_codes:
                        product_row = self.df[self.df['product_code'] == str_code]
                        price_val = float(product_row['price'].iloc[0])
                        original_prices.append(price_val)
                
                if not original_prices:
                    return 1e6
                    
                original_cost = sum(original_prices)
                fitness = original_cost * 2.0
            except Exception as e:
                fitness = 1e6
        else:
            fitness = self.aco.evaluator.evaluate(path, self.shopping_list_ids, self.restrictions)


        self.fitness_cache[key] = fitness
        print(f"  ✅ Solución encontrada | Fitness: {fitness:.2f}")
        return fitness

    def _tournament_selection(self, scored, k=3):
        contenders = random.sample(scored, min(len(scored), k))
        contenders.sort(key=lambda x: x[1])
        return contenders[0][0]

    def _blend_crossover(self, p1, p2, alpha=0.5):
        c1, c2 = [], []
        for w1, w2 in zip(p1, p2):
            d = abs(w1 - w2)
            low = min(w1, w2) - alpha * d
            high = max(w1, w2) + alpha * d
            r1 = random.uniform(low, high)
            r2 = random.uniform(low, high)
            c1.append(r1)
            c2.append(r2)
        c1_arr = np.array(c1); c2_arr = np.array(c2)
        if c1_arr.sum() > 0:
            c1 = (c1_arr / c1_arr.sum()).tolist()
        else:
            c1 = p1[:]
        if c2_arr.sum() > 0:
            c2 = (c2_arr / c2_arr.sum()).tolist()
        else:
            c2 = p2[:]
        return c1, c2

    def _mutate(self, weights):
        w = weights[:]
        for i in range(len(w)):
            if random.random() < self.mutation_rate:
                delta = random.gauss(0, 0.1 * w[i])
                w[i] = max(0.0, w[i] + delta)
        total = sum(w)
        if total > 0:
            w = (np.array(w) / total).tolist()
        else:
            w = [1/3, 1/3, 1/3]
        return w

    def run(self):
        population = self._init_population()
        best_w = None
        best_f = float('inf')

        for gen in range(self.generations):
            scored = [(ind, self._evaluate_fitness(ind)) for ind in population]
            scored.sort(key=lambda x: x[1])
            gen_best_w, gen_best_score = scored[0]

            if gen_best_score < best_f:
                best_f = gen_best_score
                best_w = gen_best_w[:]

            print(f"🔬 GA Gen {gen+1}/{self.generations} — Best fitness: {gen_best_score:.2f}")

            new_pop = [ind for ind, _ in scored[:self.elitism]]
            while len(new_pop) < self.population_size:
                parent1 = self._tournament_selection(scored, k=3)
                parent2 = self._tournament_selection(scored, k=3)
                c1, c2 = self._blend_crossover(parent1, parent2, alpha=0.5)
                new_pop.append(self._mutate(c1))
                if len(new_pop) < self.population_size:
                    new_pop.append(self._mutate(c2))
            population = new_pop

        return best_w, best_f