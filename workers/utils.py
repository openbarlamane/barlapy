import pymongo
from config import MONGO_URI

def connect_to_db():
    mongo = pymongo.MongoClient(MONGO_URI)
    db = mongo["barlamane"]
    return db

