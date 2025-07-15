import ast
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity, cosine_distances
from AI.embeddings import retrive_embedding_from_df

def parse_embedding(embedding_str):
    if isinstance(embedding_str, np.ndarray):
        return embedding_str

    if isinstance(embedding_str, list):
        return np.array(embedding_str, dtype=float)
    


    if isinstance(embedding_str, str):
        return np.array(
            [float(x) for x in embedding_str
            .replace('[', '')
            .replace(']', '')
            .replace('\n', '')
            .split()]
    )
    

    return np.array([])

def preprocess_data(df):
    df['product_code'] = df['product_code'].astype(str).str.strip()
    
    df['embedding'] = df['embedding'].apply(parse_embedding)
    
    if isinstance(df['allergens'].iloc[0], str):
        df['allergens'] = df['allergens'].apply(lambda x: ast.literal_eval(x))
    
    return df

def get_candidates(product, embeddings, df, code2idx, k=20):
    vec = retrive_embedding_from_df(product, embeddings, code2idx)
    if vec is None:
        return pd.DataFrame(), np.array([])
    
    sims = cosine_similarity(vec.reshape(1, -1), embeddings)[0]
    top_idx = np.argsort(sims)[-k:][::-1]

    productos_similares = df.iloc[top_idx][['product_code', 'name', 'price']].copy()

    productos_similares['embedding'] = productos_similares['product_code'] \
        .map(lambda code: retrive_embedding_from_df(code, embeddings, code2idx))

    return productos_similares, sims[top_idx]