
from pymongo import MongoClient
import pymongo
import operator

client = MongoClient()
mongodb = client.videos
videocol = mongodb.videos

videos = videocol.find().sort('videoInfo.statistics.viewCount',pymongo.DESCENDING)
print videos[0]['videoInfo']['id']
