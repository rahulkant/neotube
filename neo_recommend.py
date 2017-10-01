from py2neo import Graph, authenticate, Node, Relationship
import operator
from pymongo import MongoClient


client = MongoClient()
db = client.videos
collection = db.videos

authenticate("localhost:7474","neo4j","vegeta")

graph = Graph('http://localhost:7474/db/data/')
s_id = '_56kX-8pdxg'
s = "match (n1 {id:'" + s_id + "'})-[r]-(n2)  return n2.id,r.weight;"
curser = graph.run(s).data()
# print curser

d = {}
for i in curser:
	try:
		d[i['n2.id']] += int(i['r.weight'])
	except:
		d[i['n2.id']] = int(i['r.weight'])

# print d
l = list(sorted(d.items(), key=operator.itemgetter(1)))
for i in xrange(len(l)):
	l[i] = list(l[i])
	# print l[i][1]
for i in xrange(len(l)):
	for doc in collection.find({"videoInfo.id" : l[i][0]}):
		l[i][1] += int( doc['videoInfo']['statistics']['likeCount']) - int(doc['videoInfo']['statistics']['dislikeCount']) + int((doc['videoInfo']['statistics']['viewCount'])/5)

l = sorted(l,key=lambda l:l[1], reverse=True)
# print(len(l))
for i in xrange(len(l)):
	print l[i]
