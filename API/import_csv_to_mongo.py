import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "despensia_db")

df = pd.read_csv("productos_filtrados.csv")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db["despensia_collection"]

productos = df.to_dict(orient="records")
result = collection.insert_many(productos)

print(f"Se insertaron {len(result.inserted_ids)} productos.")
