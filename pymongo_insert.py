import os
from pymongo import MongoClient
import json

client = MongoClient()
db = client.videos
collection = db.videos
collection.drop()

for filename in os.listdir(os.getcwd() + "/test"):
        # print filename
        with open("test/" + filename,"r") as fp:
                s = fp.read()

        parsed_json = json.loads(s)
        id = collection.insert_one(parsed_json).inserted_id
        print id
