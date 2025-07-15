import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "despensia_db")

# Lee el CSV
df = pd.read_csv("productos_filtrados.csv")

# Conecta a MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db["despensia_collection"]  # O el nombre de la colección que uses

# Convierte cada fila del DataFrame en un dict y lo inserta
productos = df.to_dict(orient="records")
result = collection.insert_many(productos)

print(f"Se insertaron {len(result.inserted_ids)} productos.")
