'''

@author: andyh
'''
import sys
sys.path.append("..")
from Util import Util
import time
import os
import json
import Worker
import Cluster
#Default parameter 
DEFAULT_NAMELIST=["fenghuang","xinhua","sina","sohu","net"]
#The default vector size of news 
DEFAULT_VECTOR_SIZE=300
# The news with sum(vector)<weight_limit will not be processed 
DEFAULT_WEIGHT_LIMIT=0.05
# The merger limit of news. If two news has similarity larger than this limit, 
# these two news will be merged
DEFAULT_MERGE_LIMIT=0.95
DEFAULT_CLUSTER_RESULT_FILENAME="clusterResult"
def sleeptime(hour, minu, sec):
    return hour * 3600 + minu * 60 + sec
def getNameList():
    tempNameList=DEFAULT_NAMELIST.copy()
    currentDate=Util.getDateInStr()
    fileLocation=Util.getDataPath()+currentDate+os.sep
    fileType=".json"
    for i in range(len(tempNameList)):
        tempNameList[i]=fileLocation+tempNameList[i]+currentDate+fileType
    resultNameList=list()
    for i in range(len(tempNameList)):
        try:
            tempFile=open(tempNameList[i],'r')
            tempFile.close()
        except:
            print(tempNameList[i]+" is no found")
            continue
        resultNameList.append(tempNameList[i])
    return resultNameList

def doAnalysis(vectorSize=DEFAULT_VECTOR_SIZE,weightLimit=DEFAULT_WEIGHT_LIMIT,mergeLimit=DEFAULT_MERGE_LIMIT):
    # Get the name list of to be processed file 
    nameList=getNameList()
#     for item in nameList:
#         print(item)
    if(nameList==None or len(nameList)==0):
        print("No data for clustering")
        return
    
    # Load the data
    worker=Worker.Worker()
    
    for filename in nameList:
        data=worker.loadData(filename)
        worker.addNews(data)
#         worker.printAllNews()
        keywordDict=worker.getKeyWordDict()
        pass
    print("len(keywordDict):"+str(len(keywordDict)))
#     convert the news into vector
    newsVectorList=worker.vectorLization(vectorSize,weightLimit=weightLimit)
    #The all news set
    newsList=worker.getAllNews()
    
    #clustering
    cluster=Cluster.Cluster(newsVectorList=newsVectorList)
    newsMergedList=cluster.getHierResult(mergeLimit=mergeLimit)
    resultNewsList=list()
    for i in range(len(newsMergedList)):
        print("Cluster:"+str(i))
        itemList=newsMergedList[i]
        tempNewsList=list()
        for newsID in itemList:
            news=newsList[newsID]
            print(news.toString())
            tempNewsList.append(news.toDict())
        resultNewsList.append(tempNewsList)   
    exportResultToDisk(resultNewsList)
    
def exportResultToDisk(resultNewsList):
    clusterResultFileName=DEFAULT_CLUSTER_RESULT_FILENAME
    fileType=".json"
    outputFath=Util.getDataPath()+Util.getDateInStr()+os.sep+clusterResultFileName+fileType
    l=len(resultNewsList)
    with open(outputFath, 'w') as outfile:
        outfile.write('[')
        for i in range(l):
            newsList=resultNewsList[i]
            outfile.write("{\"clusterId\":"+str(i))
            outfile.write(",")
            outfile.write("\"data\":")
            outfile.write('[')
            for j in range(len(newsList)-1):
                json.dump(newsList[j], outfile, ensure_ascii=False)
                outfile.write(',')
            json.dump(newsList[-1], outfile, ensure_ascii=False)
            outfile.write(']}')
            if(i<l-1):
                outfile.write(",")
        outfile.write(']')
    pass
if __name__ == '__main__':
    second = sleeptime(0, 0, 10)
    while(True):
        doAnalysis()
        time.sleep(second)
    pass