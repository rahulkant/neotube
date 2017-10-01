import os
import json
# from py2neo import Graph,authenticate, Node, Relationship
from py2neo import Graph, authenticate, Node, Relationship

authenticate("localhost:7474","neo4j","vegeta")

graph = Graph('http://localhost:7474/db/data/')

keys = [
        'videoInfo',
        'snippet',
        'channelId',
        'tags',
        'channelTitle',
        'title',
        'description',
        'id',
        'etag',
        'statistics',
        'commentCount',
        'viewCount',
        'favoriteCount',
        'dislikeCount',
        'likeCount'
]

nodes = []
neo_nodes = []
neo_relationships = []

for filename in os.listdir(os.getcwd() + "/test"):
        # print filename
        with open("test/" + filename,"r") as fp:
                s = fp.read()

        parsed_json = json.loads(s)

        data = {}

        videoInfo = parsed_json[keys[0]]
        snippet = videoInfo[keys[1]]

        data[keys[2]] = snippet[keys[2]]

        if keys[3] in snippet.keys():
                data[keys[3]] = snippet[keys[3]]
        else:
                data[keys[3]] = []

        data[keys[4]] = snippet[keys[4]]
        data[keys[5]] = snippet[keys[5]]
        data[keys[6]] = snippet[keys[6]]

        data[keys[7]] = videoInfo[keys[7]]
        data[keys[8]] = videoInfo[keys[8]]

        statistics = videoInfo[keys[9]]

        data[keys[10]] = int(statistics[keys[10]])
        data[keys[11]] = int(statistics[keys[11]])
        data[keys[12]] = int(statistics[keys[12]])
        data[keys[13]] = int(statistics[keys[13]])
        data[keys[14]] = int(statistics[keys[14]])

        nodes.append(data)
        # temp_Node = Node('VIDEO',id = data['id'],viewCount = data['viewCount'], likeCount = data['likeCount'], dislikeCount = data['dislikeCount'], favoriteCount = data['favoriteCount'], commentCount = data['commentCount'], channelId = data['channelId'], description = data['description'], tags = data['tags'])

        temp_Node = Node('VIDEO',id = data['id'],viewCount = data['viewCount'], likeCount = data['likeCount'], dislikeCount = data['dislikeCount'], favoriteCount = data['favoriteCount'], commentCount = data['commentCount'])
        neo_nodes.append(temp_Node)

        # print temp_Node,', '

channelIds = []


for x in nodes:
        if not (x['channelId'] in channelIds):
                channelIds.append(x['channelId'])


for x in channelIds:
        sameChannelVideos = []
        for y in range(0,len(nodes)):
                if nodes[y]['channelId'] == x:
                        sameChannelVideos.append(y)
        # print sameChannelVideos
        for i in range(0,len(sameChannelVideos)):
                for j in range(i+1,len(sameChannelVideos)):
                        temp_Relationship = Relationship(neo_nodes[sameChannelVideos[i]],'SAME_CHANNEL',neo_nodes[sameChannelVideos[j]],weight = 10)
                        neo_relationships.append(temp_Relationship)
#                                 # print temp_Relationship
#
for x in range(0,len(nodes)):
        for y in range(x+1,len(nodes)):
                weight = 0

                text1 = nodes[x]['description']
                text2 = nodes[y]['description']

                words1 = text1.split()
                words2 = text2.split()

                common = set(words1).intersection(set(words2))
                weight = len(common)

                if weight > 0:
                        temp_Relationship = Relationship(neo_nodes[x],'SIMILAR_DESC',neo_nodes[y],weight = weight)
                        neo_relationships.append(temp_Relationship)
#                         # print temp_Relationship


for x in range(0,len(nodes)):
        for y in range(x+1,len(nodes)):
                weight = 0

                text1 = nodes[x]['title']
                text2 = nodes[y]['title']

                words1 = text1.split()
                words2 = text2.split()

                common = set(words1).intersection(set(words2))
                weight = len(common)

                if weight > 0:
                        temp_Relationship = Relationship(neo_nodes[x],'SIMILAR_TITLE',neo_nodes[y],weight = weight)
                        neo_relationships.append(temp_Relationship)

                        # print temp_Relationship

for x in range(0,len(nodes)):
        for y in range(x+1,len(nodes)):
                weight = 0

                tag1 = nodes[x]['tags']
                tag2 = nodes[y]['tags']

                common = set(tag1).intersection(set(tag2))
                weight = len(common)

                if weight > 0:
                        temp_Relationship = Relationship(neo_nodes[x],'COMMON_TAGS',neo_nodes[y],weight = weight)
                        neo_relationships.append(temp_Relationship)

                        # print temp_Relationship

print "Nodes to create : " + str(len(neo_nodes))
print "Relationships to create : " + str(len(neo_relationships))

rels_count = len(neo_relationships)
node_count = len(neo_nodes)

graph.delete_all()


tx = graph.begin()
count = 0
for n in neo_nodes:
        count +=1
        print "node ",count," inserted out of ",node_count
        tx.create(n)
tx.commit()

tx = graph.begin()
count = 0
relationship_count = 0
for r in neo_relationships:
        count +=1
        relationship_count += 1
        if count == 10000:
            count = 0
            tx.commit()
            tx = graph.begin()
        print "relationship ",relationship_count," inserted out of ",rels_count
        tx.create(r)

tx.commit()

print "Graph created"
