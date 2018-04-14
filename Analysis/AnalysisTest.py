'''

@author: andyh
'''
import Worker
import json
import numpy as np
from Util import Util 
import Cluster
if __name__ == '__main__':
#     nameList=["fenghuang321.json","xinhua321.json","sina321.json","sohu321.json","xinhua321.json"]
#     nameList=["fenghuang322.json","xinhua322.json","sina322.json","sohu322.json","net322.json"]
#     nameList=["fenghuang323.json","xinhua323.json","sina323.json","sohu323.json","net323.json"]
    nameList=["fenghuang42.json","xinhua42.json","sina42.json","sohu42.json","net42.json"]
    nameList=["fenghuang44.json","xinhua44.json","sina44.json","sohu44.json","net44.json"]
#     nameList=["test2.json"]
    worker=Worker.Worker()
    
    for name in nameList:
        filename=Util.getDataPath("testData\\44\\"+name)
        data=worker.loadData(filename)
        worker.addNews(data)
#         worker.printAllNews()
        keywordDict=worker.getKeyWordDict()
#         print(keywordDict)
    print("len(keywordDict):"+str(len(keywordDict)))
    vectorSize=300
    weightLimit=0
#     vectorSize=len(worker.getKeyWordDict())-1

#keyword that will be used in encoding a news
    globalKeywordList,globalValueList=worker.getTopKKeywordList(vectorSize)
    for i in range(len(globalKeywordList)):
#         print(str(i)+" "+globalKeywordList[i]+" "+str(globalValueList[i]))
#         for j in range(globalValueList[i]):
#             print(globalKeywordList[i])
        pass
    
    sortGlobalKeywordList=globalKeywordList
    sortGlobalValueList=globalValueList
    Worker.sortKeyword(sortGlobalKeywordList, sortGlobalValueList, "ByKeyword")
#     for keyword in sortGlobalKeywordList:
#         print(keyword)

    print("vectorSize:"+str(vectorSize))
#     worker.printAllNews()
    newsVectorList=worker.vectorLization(vectorSize,weightLimit=weightLimit)
#     for vector in newsVectorList:
#         print(vector.toString())
    l=len(newsVectorList)
    print("Number of news:"+str(l))
    
#     testSet=[35,46,92,93]
    testSet=range(0,l)
    #The all news set
    newsList=worker.getAllNews()
    
    targetId=70
    print("Target news id: "+str(targetId))
    print("Target new info:")
    print(newsList[targetId].toString())
    targetVector=newsVectorList[targetId].newsVector
    limit=0.2
    for i in testSet:
        similarity=Cluster.Cluster.getVectorSimilarity(targetVector, newsVectorList[i].newsVector, strategy="Cos")
        if(similarity>=limit):
            
            newsId=newsVectorList[i].newsId
            print("New id:"+str(newsId))
            print("similarity to news "+str(targetId)+":"+str(similarity))  
            
            
            news=newsList[newsId]
            print(news.toString())
            #print the encode details
            for j in range(len(newsVectorList[i].newsVector)):
                if(newsVectorList[i].newsVector[j]>0):
                    print(sortGlobalKeywordList[j]+" "+str(newsVectorList[i].newsVector[j]))

    
#     kmeans cluster test
#     cluster=Cluster.Cluster(newsVectorList=newsVectorList)
#     k=10
#     centerList,assignementList,cost=cluster.getKMeansResult(k)
#        
#     outputfilename="testout.txt"
#     f=open(outputfilename,'w')
#     for i in range(k):
#         f.write("cluster:"+str(i)+"\n")
#         clusterNewsList=assignementList[i]
#         center=centerList[i]
#         for news in clusterNewsList:
#             similarity=np.dot(center,news.newsVector)/(np.linalg.norm(center)*(np.linalg.norm(news.newsVector)))
#    
#             newsId=news.newsId
#             newsInfo=newsList[newsId]
#             f.write(newsInfo.title+"\n")
#             f.write(newsInfo.jump+"\n")
#             f.write("similarity"+str(similarity)+"\n")
#     f.close()
    #hier cluster
    
    #Test data
#     testVectorList=list()
#     testVectorList.append(Worker.newsInfo(1,[1,1,0,0,0]))
#     testVectorList.append(Worker.newsInfo(2,[1,0.8,0,0,0]))
#     testVectorList.append(Worker.newsInfo(3,[0,1,2,2,0]))
#     testVectorList.append(Worker.newsInfo(4,[0,0,2,2,0]))
#     testVectorList.append(Worker.newsInfo(5,[0,0,0,0,1]))
#     newsVectorList=testVectorList
    
    cluster=Cluster.Cluster(newsVectorList=newsVectorList)
    print("Clustering result")
    limit=0.9
    k=20
    newsMergedList=cluster.getHierResult(k,limit)
    count=0
    for itemList in newsMergedList:
        if(len(itemList)<2):
            continue
        print("Cluster:"+str(count))
        count=count+1
        for newsID in itemList:
            news=newsList[newsID]
            print("new ID:"+str(newsID))
            print(news.title)
            print(news.jump)
#             print(news.keywordList)
#             print(news.valueList)
#             for i in range(len(newsVectorList)):
#                 if(newsVectorList[i].newsId==newsID):
#                     print(newsVectorList[i].newsVector)

            
            
    
    
    