from pymongo import MongoClient
import os

uri = "mongodb+srv://qnrhd99_db_user:wj7JZUImwedq0x0E@teama.k58xklb.mongodb.net/UCSI_DB?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client['UCSI_DB']

print(f"Collections: {db.list_collection_names()}")
for coll_name in db.list_collection_names():
    print(f"\nCollection: {coll_name}")
    doc = db[coll_name].find_one()
    print(f"Sample: {doc}")
