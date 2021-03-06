from pymongo import MongoClient
import random

def connectMongo():
    client = MongoClient('API key')
    db = client.get_database('RUHacksDB')
    src = db.source
    return src

def addtoDB(tuple,src):
    if not list(src.find({"name": tuple[0],"phone": tuple[1],"faddr": tuple[2],"placeId": tuple[3],"coords": tuple[4]})):
        print("adding")
        db_toAdd = {
            "name": tuple[0],
            "phone": tuple[1],
            "faddr": tuple[2],
            "placeId": tuple[3],
            "coords": tuple[4]
        }
        src.insert(db_toAdd)
    else:
        print("its in already????")

def randomDB(src):
    res = list(src.find({}))
    return res[random.randint(0, len(res) - 1)]

print(randomDB(connectMongo()))
