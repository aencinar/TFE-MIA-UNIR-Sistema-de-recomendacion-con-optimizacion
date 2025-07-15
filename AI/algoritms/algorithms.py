def greedy_fallback(shopping_ids, budget, restrictions, df, neighbors_dict):
    path, cost = [], 0.0

    for code in shopping_ids:
        candidates = neighbors_dict.get(int(code), [])
        valid = []
        for nbr in candidates:
            matches = df.loc[df["product_code"] == str(nbr)]
            if not matches.empty:
                row = matches.iloc[0]
                if row["price"] + cost <= budget and all(
                    (r == 0) or (row["allergens"][i] == 1)
                    for i, r in enumerate(restrictions or [])
                ):
                    valid.append((nbr, float(row["price"])))
            else:
                print(f"[WARN] Código {nbr} no encontrado en el dataframe")
        if not valid:
            matches = df.loc[df["product_code"] == code]
            if not matches.empty:
                path.append(code)
                cost += float(matches["price"].iloc[0])
            else:
                print(f"[ERROR] Código {code} no encontrado en el dataframe, se omite.")
        else:
            nbr, p = min(valid, key=lambda x: x[1])
            path.append(nbr)
            cost += p
    return path, cost
