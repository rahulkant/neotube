from django.http import HttpResponse
from django.shortcuts import render , redirect
from django.conf import settings

# mongo imports
from pymongo import MongoClient
import pymongo
import operator
import math
# neo4j imports
from py2neo import Graph, authenticate, Node, Relationship



client = MongoClient()
mongodb = client.search_engine
videos = mongodb.videos
db = client.videos
collection = db.videos

authenticate("localhost:7474","neo4j","vegeta")
graph = Graph('http://localhost:7474/db/data/')
#
# most_viewed = videos[0]['videoInfo']['id']

def index(request):
	flag = True
	videos_per_page = 20.0
	if not request.user.is_authenticated():
		flag = False
	top_videos = videos.find().sort('videoInfo.statistics.viewCount',pymongo.DESCENDING)
	show_videos = []
	for t in top_videos:
		description = t['videoInfo']['snippet']['localized']['title']
		t['videoInfo']['snippet']['localized']['title'] = description[:50] + "..."
		show_videos.append(dict(t))

	if 'page' not in request.GET.keys():
		page = 1;
	elif int(request.GET['page'])*videos_per_page > len(show_videos):
		page = len(show_videos)/videos_per_page
	elif int(request.GET['page'])*videos_per_page <=0:
		page = 1
	else:
		page = int(request.GET['page'])

	# print top_videos
	return render(request,'neoyoutube/show.html',
	{
	'flag':flag,
	'show_videos':show_videos[int((page-1)*videos_per_page):int(page*videos_per_page)],
	'page': page,
	'page_range':range(1,int(math.ceil(len(show_videos)/videos_per_page)) + 1),
	'num_results':len(show_videos)
	})
	# return HttpResponse("Hello, world. You're at the polls index.")

def watch_view(request):
	flag = True
	if not request.user.is_authenticated():
		flag = False
	if 'id' not in request.GET.keys():
		return redirect('/')

	id = request.GET['id']


	# print id
	data = dict(videos.find_one({'videoInfo.id': id}))
	s_id = id
	s = "match (n1 {id:'" + s_id + "'})-[r]-(n2)  return n2.id,r.weight;"
	curser = graph.run(s).data()
	# print curser
	update_document = videos.find_one({'videoInfo.id' : id})
	viewCount = update_document['videoInfo']['statistics']['viewCount']
	# print viewCount
	videos.update({'videoInfo.id':id}, {"$set": {'videoInfo.statistics.viewCount': int(viewCount) + 1}}, upsert=False)

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
			l[i][1] += int( doc['videoInfo']['statistics']['likeCount']) - int(doc['videoInfo']['statistics']['dislikeCount']) + int((doc['videoInfo']['statistics']['viewCount'])/50)

	l = sorted(l,key=lambda l:l[1], reverse=True)
	# print(len(l))
	recommends = []
	for i in xrange(len(l)):
		v_data = dict(videos.find_one({'videoInfo.id' : l[i][0]}))
		recommends.append(v_data)
	# print recommends
	return render(request,"neoyoutube/watch.html",{'id':id,'data':data,'recommends':recommends , 'flag':flag})

def search_query_view(request):
	videos_per_page = 10.0
	flag = True
	if not request.user.is_authenticated():
		flag = False

	if 'search' not in request.GET.keys():
		return redirect('/')

	query = request.GET['search']
	if len(query) == 0:
		return redirect('/')

	result = videos.aggregate([
			{ "$match": { "$text": { "$search": query } } },
			{ "$sort": { "score": { "$meta": "textScore" } } },
			{ "$project": { "videoInfo.id": 1, "_id":0, "score": { "$meta": "textScore" }} }
	   	])

	video_data = []
	for res in result:
		# print res["videoInfo"]["id"], res["score"]
		data = dict(videos.find_one({'videoInfo.id' : res['videoInfo']['id']}))
		description = data['videoInfo']['snippet']['localized']['description']
		data['videoInfo']['snippet']['localized']['description'] = description[:200] + "...."
		# print data['videoInfo']['snippet']['localized']['description']
		video_data.append(data)


	if 'page' not in request.GET.keys():
		page = 1;
	elif int(request.GET['page'])*videos_per_page > len(video_data):
		page = int(math.ceil(len(video_data)/videos_per_page))
	elif int(request.GET['page'])*videos_per_page <=0:
		page = 1
	else:
		page = int(request.GET['page'])

 	return render(request,"neoyoutube/search.html",
	{
	'video_data' : video_data[int((page-1)*videos_per_page):int(page*videos_per_page)],
	# 'video_data' : video_data,
	'query' : query ,
	'flag' : flag,
	'page': page,
	'page_range':range(1,int(math.ceil(len(video_data)/videos_per_page)) + 1),
	'num_results':len(video_data)
	})

def channel_view(request):

	videos_per_page = 20.0
	flag = True
	if not request.user.is_authenticated():
		flag = False

	if 'channelid' not in request.GET.keys():
		return redirect('/')

	channelid = request.GET['channelid']
	if len(channelid) == 0:
		return redirect('/')

	channel_videos = []
	video_cursor = videos.find({'videoInfo.snippet.channelId' : channelid})
	for data in video_cursor:
		channel_videos.append(dict(data))

	if 'page' not in request.GET.keys():
		page = 1;
	elif int(request.GET['page'])*videos_per_page > len(channel_videosvideo):
		page = int(math.ceil(len(channel_videos)/videos_per_page))
	elif int(request.GET['page'])*videos_per_page <=0:
		page = 1
	else:
		page = int(request.GET['page'])

 	return render(request,"neoyoutube/channel.html",
	{
	'channel_videos' : channel_videos[int((page-1)*videos_per_page):int(page*videos_per_page)],
	'channelid' : channelid ,
	'flag' : flag,
	'page': page,
	'num_results':len(channel_videos)
	})
