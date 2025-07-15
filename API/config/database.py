from pymongo import MongoClient, errors
from dotenv import load_dotenv
import os
import ssl

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "despensia_db")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000, ssl=True)
    client.server_info()
    print("Conectado a MongoDB Atlas")
except errors.ServerSelectionTimeoutError as error:
    print("Error al conectar con MongoDB:", error)
    raise

db = client[DB_NAME]
collection_name = db["despensia_collection"]