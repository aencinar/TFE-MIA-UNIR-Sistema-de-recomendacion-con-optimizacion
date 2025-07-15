import time
from AI.evaluate_solution import evaluate_solution, evaluate_with_metrics
from AI.utils import get_candidates, preprocess_data
from AI.algoritms.algorithms import greedy_fallback
from AI.algoritms.evaluator import MultiObjectiveEvaluator
from AI.algoritms.ACO_algorithm import AntColony
from AI.algoritms.GA_algorithm import GeneticOptimizer


def search(products_list, budget, restrictions, df, graphs_by_cluster, neighbors_dict, embeddings, code2idx):
    shopping_codes = []

    df_processed = preprocess_data(df)

    for item in products_list:
        productos_similares, sims = get_candidates(item, embeddings, df_processed, code2idx)
        if not productos_similares.empty:
            best_candidate = productos_similares.iloc[0]['product_code']
            shopping_codes.append(best_candidate)
        else:
            shopping_codes.append(item)


    shopping_codes = list(set(shopping_codes))
    print(f"🛒 Total de códigos iniciales: {len(shopping_codes)}")

    valid_codes = set(df_processed['product_code'])
    valid_shopping_codes = [code for code in shopping_codes if code in valid_codes]
    
    print(f"✅ Códigos válidos encontrados: {len(valid_shopping_codes)}/{len(shopping_codes)}")
    if len(valid_shopping_codes) == 0:
        print("🚨 No hay códigos válidos para buscar. Usando fallback.")
        return greedy_fallback(shopping_codes, budget, restrictions, df_processed, neighbors_dict)
    
    start = time.time()

    evaluator = MultiObjectiveEvaluator(df_processed, weights=(1.0, 1.0, 1.0), budget=budget)

    aco_fast = AntColony(
        graphs_by_cluster=graphs_by_cluster,
        df=df_processed,
        evaluator=evaluator,
        neighbors_dict=neighbors_dict,
        alpha=1.0,
        beta=2.0,
        evaporation_rate=0.1,
        pheromone_init=0.1,
        q=1.0
    )

    ga = GeneticOptimizer(
        fast_aco=aco_fast,
        df = df_processed,
        shopping_list_ids=products_list,
        budget=budget,
        restrictions=restrictions,
        population_size=10,
        generations=5,
        mutation_rate=0.1,
        elitism=1
    )
    best_weights, best_fitness = ga.run()

    evaluator.set_weights(best_weights)
    final_path, final_cost = aco_fast.run(
        shopping_list_ids=products_list,
        budget=budget,
        restrictions=restrictions,
        n_ants=5,
        n_iterations=5
    )

    end = time.time()

    print(f"⏱️ Tiempo total de ejecución: {end - start:.3f} segundos")

    metrics = evaluate_solution(
        products_list,           # lista original
        final_path,              # solución propuesta
        evaluator,               # evaluador
        restrictions,            # restricciones binarias
        df_processed,            # dataframe procesado
        start, end
    )

    fitness_original = evaluator.evaluate(products_list, products_list, restrictions)

    print("fitness original ",fitness_original)

    print("metricas ",metrics)

    if final_path is None:
        #fallback
        print("NO RESULTADO ACO/GA")
        final_path, final_cost = greedy_fallback(
            shopping_codes,
            budget,
            restrictions,
            df_processed,
            neighbors_dict
        )
        best_weights = None

    return final_path, final_cost, best_weights