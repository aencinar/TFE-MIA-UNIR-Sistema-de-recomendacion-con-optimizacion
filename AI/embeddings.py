import numpy as np

category_columns = [f'category_{i}' for i in range(1, 41)]
supermarket_columns = [f'supermarket_{name}' for name in ['Alcampo', 'Eroski', 'Mercadona']]

def load_embeddings(path="AI/embeddings.npy"):
    return np.load(path)

def get_embedding(idx, embeddings):
    return embeddings[idx]

def get_enriched_embedding(row):
    text = row['name_clean'].lower()
    text_embed = get_embedding(text)

    cat_vec = np.array([row[col] for col in category_columns], dtype=np.float32)
    sup_vec = np.array([row[col] for col in supermarket_columns], dtype=np.float32)
    allergen_vec = np.array(row["allergens"], dtype=np.float32)
    price = np.array([row["price_norm"]], dtype=np.float32)

    enriched = np.concatenate([text_embed, price, cat_vec, sup_vec, allergen_vec])
    return enriched

def retrive_embedding_from_df(product_code, embeddings, code2idx):
    key = str(product_code).strip()
    idx = code2idx.get(key)
    if idx is None:
        return None
    vec = embeddings[idx]
    return np.array(vec, dtype=np.float32).flatten()

