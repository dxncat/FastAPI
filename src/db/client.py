from pymongo import MongoClient
from decouple import config

db_client = MongoClient(config("MONGODB_URI")).ecommerce