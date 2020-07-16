import pymongo

def connect_to_db():
    mongo = pymongo.MongoClient("mongodb+srv://marrakchino:tfou3lik@cluster0-8swuh.mongodb.net/test:barlamane")
    db = mongo["barlamane"]
    return db

