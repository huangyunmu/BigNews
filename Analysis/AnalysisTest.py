'''

@author: andyh
'''
import Worker
import json
import numpy as np
from Util import DataLoader 
import Cluster
if __name__ == '__main__':
#     nameList=["fenghuang321.json","xinhua321.json","sina321.json","sohu321.json","xinhua321.json"]
#     nameList=["fenghuang322.json","xinhua322.json","sina322.json","sohu322.json","net322.json"]
#     nameList=["fenghuang323.json","xinhua323.json","sina323.json","sohu323.json","net323.json"]
    nameList=["fenghuang42.json","xinhua42.json","sina42.json","sohu42.json","net42.json"]
#     nameList=["test2.json"]
    worker=Worker.Worker()
    
    for name in nameList:
        filename=DataLoader.getDataPath("testData\\42\\"+name)
        data=worker.loadData(filename)
        worker.addNews(data)
#         worker.printAllNews()
        keywordDict=worker.getKeyWordDict()
#         print(keywordDict)
    print("len(keywordDict):"+str(len(keywordDict)))
    print("worker.getTopKKeywordDict(k)")
    vectorSize=200
    weightLimit=0.05
#     vectorSize=len(worker.getKeyWordDict())-1
    print(worker.getTopKKeywordDict(vectorSize))
    print("vectorSize:"+str(vectorSize))
    newsVectorList=worker.vectorLization(vectorSize,weightLimit=weightLimit)
#     for vector in newsVectorList:
#         print(vector.toString())
    l=len(newsVectorList)
    print("Number of news:"+str(l))
    
#     testSet=[0,18,19,20]
    testSet=range(0,l)
    newsList=worker.getAllNews()
#     testTarget=51
#     vector1=newsVectorList[testTarget].newsVector
#     limit=0.5
#     for i in testSet:
#         similarity=np.dot(vector1,newsVectorList[i].newsVector)/(np.linalg.norm(vector1)*(np.linalg.norm(newsVectorList[i].newsVector)))
#         if(similarity>limit):
#             print(i)
#             print("similarity to news "+str(testTarget)+":"+str(similarity))
#             newsId=newsVectorList[i].newsId
#             news=newsList[newsId]
#             print(news.toString())
    
    
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
    cluster=Cluster.Cluster(newsVectorList=newsVectorList)
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
#             print(news.jump)
#             print(news.keywordList)
#             print(news.valueList)
#             for i in range(len(newsVectorList)):
#                 if(newsVectorList[i].newsId==newsID):
#                     print(newsVectorList[i].newsVector)
            
            
    
    
    