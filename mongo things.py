from pymongo import MongoClient
import json
import os

client = MongoClient()
db = client.search_engine
videos = db.videos

directory = 'test/'

i=1

for filename in os.listdir(directory):
    json_data = open(directory + filename).read()
    video = json.loads(json_data)
    video_id = videos.insert_one(video).inserted_id
    print str(i) + " --> ", video_id
    i+=1




db.videos.createIndex(
   {
     "videoInfo.snippet.title": "text",
     "videoInfo.snippet.channelTitle": "text",
     "videoInfo.snippet.description": "text",
     "videoInfo.snippet.tags": "text"
   },
   {
     weights: {
      "videoInfo.snippet.title": 10,
     "videoInfo.snippet.channelTitle": 6,
     "videoInfo.snippet.description": 2,
     "videoInfo.snippet.tags": 4
     },
     name: "video_index"
   }
 )

from pymongo import MongoClient

client = MongoClient()
db = client.search_engine
videos = db.videos

query = str(raw_input("Enter Search query: "))

result = videos.aggregate([
		{ "$match": { "$text": { "$search": query } } },
		{ "$sort": { "score": { "$meta": "textScore" } } },
		{ "$project": { "_id": 1,  "score": { "$meta": "textScore" }} }
   	])

for res in result:
	print res["_id"], res["score"]
