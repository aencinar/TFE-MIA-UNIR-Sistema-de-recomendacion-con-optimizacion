import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def evaluate_solution(shopping_list, result_path, evaluator, restrictions, df, start_time=None, end_time=None):
    # Fitness
    shopping_list = [str(code).strip() for code in shopping_list]
    fitness = evaluator.evaluate(result_path, shopping_list, restrictions)

    # total cost
    code2row = {str(row['product_code']).strip(): row for _, row in df.iterrows()}
    total_cost = 0.0
    costs = []
    for code in result_path:
        row = code2row.get(str(code).strip())
        price = float(row['price']) if row is not None else np.nan
        total_cost += price
        costs.append(price)
    
    # average similarity
    similarities = []
    for orig, sub in zip(shopping_list, result_path):
        row_o = code2row.get(str(orig).strip())
        row_s = code2row.get(str(sub).strip())
        if row_o is not None and row_s is not None:
            emb_o = np.array(row_o['embedding']).reshape(1, -1)
            emb_s = np.array(row_s['embedding']).reshape(1, -1)
            sim = cosine_similarity(emb_o, emb_s)[0,0]
            similarities.append(sim)
    avg_sim = np.mean(similarities) if similarities else None


    # Percentage of restrictions
    total_checked = 0
    total_ok = 0
    for code in result_path:
        row = code2row.get(str(code).strip())
        if row is not None and restrictions:
            allergens = row['allergens']
            for i, r in enumerate(restrictions):
                if r == 1:
                    total_checked += 1
                    if i < len(allergens) and allergens[i] == 0:
                        total_ok += 1
    restriction_accuracy = (total_ok / total_checked * 100) if total_checked > 0 else None

    # execution time
    elapsed_time = end_time - start_time if (start_time is not None and end_time is not None) else None

    # Print summary
    print("------ EVALUACIÓN DE LA SOLUCIÓN ------")
    print(f"Fitness: {fitness:.2f}")
    print(f"Coste total: {total_cost:.2f} €")
    print(f"Similitud media: {avg_sim:.3f}" if avg_sim is not None else "Similitud media: N/A")
    if restriction_accuracy is not None:
        print(f"Restricciones cumplidas: {restriction_accuracy:.2f}%")
    if elapsed_time is not None:
        print(f"Tiempo de ejecución: {elapsed_time:.2f} s")
    print("----------------------------------------")

    return {
        'fitness': fitness,
        'total_cost': total_cost,
        'avg_similarity': avg_sim,
        'restriction_accuracy': restriction_accuracy,
        'elapsed_time': elapsed_time,
    }




def evaluate_with_metrics(shopping_list, result_path, evaluator, restrictions, fitness_max, final_time):
    fitness = evaluator.evaluate(result_path, shopping_list, restrictions)

    accuracy = (fitness / fitness_max) * 100 if fitness_max else None

    metrics = {
        'fitness': fitness,
        'accuracy_pct': accuracy,
        'time_s': final_time
    }
    print(f"→ Accuracy: {accuracy:.2f} %, Tiempo: {final_time:.3f}s")
    return metrics