import pandas as pd

def load_csv(path='AI/productos_procesados.csv'):
    df = pd.read_csv(path, delimiter=',')
    return df