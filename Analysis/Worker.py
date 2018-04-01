#coding:utf-8
'''

@author: andyh
'''
import json
import math
import numpy as np
def sortKeyword(keywordList, valueList):
        """
        To be updated
        """
        for i in range(len(keywordList)):
            for j in range(0, i):
                if(keywordList[i] < keywordList[j]):
                    temp = keywordList[i]
                    keywordList[i] = keywordList[j]
                    keywordList[j] = temp
                    temp = valueList[i]
                    valueList[i] = valueList[j]
                    valueList[j] = temp
class news(object):
    def __init__(self, title, jump, keywords, values):
        self.title = title
        self.jump = jump
        self.keywordList = keywords
        self.valueList = values
        sortKeyword(self.keywordList, self.valueList)
    
        
    def toString(self):
        result = ""
        result = result + "title:" + self.title + "\n"
        result = result + "jump:" + self.jump + "\n"
        for i in range(len(self.keywordList)):
            result = result + str(self.keywordList[i]) + " " + str(self.valueList[i]) + ","
        result = result + "\n"
        return result
class newsInfo(object):
    def __init__(self,newsId,newsVector):
        self.newsId=newsId
        self.newsVector=np.array(newsVector)
    def toString(self):
        result=""
        result=result+"newsId:"+str(self.newsId)+"\n"
        l=self.newsVector.shape[0]
        for i in range(l):
            result=result+str(self.newsVector[i])+" "
        result=result+"\n"
        return result
class Worker(object):
    
    def __init__(self):
        self.keywordDict = dict()
        self.newsList = list()
#         self.vectorSize=vectorSize
    def addNews(self, dataObject):
        currentNewsList = list()
        for item in dataObject:
            keywords = item["keywords"]
            if(len(keywords) == 1):
                continue
            else:
                l = len(keywords)
                i = 0
                keywordList = list()
                valueList = list()
                while(i < l):
                    keyword = keywords[i]
                    value = keywords[i + 1]
                    keywordList.append(keyword)
                    valueList.append(value)
                    i = i + 2
                currentNewsList.append(news(title=item["title"], jump=item["jump"], keywords=keywordList, values=valueList))
        self.newsList = self.newsList + currentNewsList
        self.updateKeywordDict(currentNewsList)
    def printAllNews(self, filename=None):
        for news in self.newsList:
            if(filename == None):
                print(news.toString())
    def getAllNews(self):
        return self.newsList
    def updateKeywordDict(self, currentNewsList):
        for news in currentNewsList:
            l = len(news.keywordList)
            for i in range(l - 1):
                keyword = news.keywordList[i]
                if(keyword in self.keywordDict):
                    self.keywordDict[keyword] = self.keywordDict[keyword] + news.valueList[i]
                else:
                    self.keywordDict[keyword] = news.valueList[i]        
    def getKeyWordDict(self):
        return self.keywordDict  
    def getTopKKeywordDict(self, vectorSize=0):
        result = dict()
        if(vectorSize == 0):
            vectorSize = self.vectorSize
        tempResult = sorted(self.keywordDict.values(), reverse=True)
        if(vectorSize < len(tempResult) - 1):
            vectorSize = len(tempResult) - 1
        limit = tempResult[vectorSize]
#         print(limit)
        for key, value in  self.keywordDict.items():
            if(value > limit):
                result[key] = value
        return result, vectorSize
    @staticmethod
    def loadData(filename):
        with open(filename) as f:
            json_str = f.read()
            data = json.loads(json_str)
        return data
    def getSortedkeywordList(self):
        keywordList = list()
        valueList = list()
        for key, value in self.keywordDict.items():
            keywordList.append(key)
            valueList.append(value)
        sortKeyword(keywordList, valueList)
        return keywordList,valueList
    def vectorLization(self, vectorSize=20,weightLimit=0.8):
        keywordList,valueList=self.getSortedkeywordList()
        l = len(keywordList)
        if(vectorSize > l):
            vectorSize = l
        keywordList = keywordList[0:vectorSize]
        valueList = valueList[0:vectorSize]
#         print("Test")
#         print("vectorSize"+str(vectorSize))
#         print("len"+str(len(keywordList)))
#         print("IDF")
        IDFList=Worker.getIDF(keywordList, valueList)
#         print("len IDF")
#         print(len(IDFList))
        newsInfoList=list()
        for i in range(len(self.newsList)):
            news=self.newsList[i]
            newsKeywordList=news.keywordList
            newsValueList=news.valueList
            newsId=i
            newsVectorData=list()
            j=0
            k=0
            while(j<vectorSize):
                if(k<len(newsKeywordList) and keywordList[j]==newsKeywordList[k]):
#                     print(newsValueList[k])
#                     print(IDFList[j])
                    newsVectorData.append(newsValueList[k]*IDFList[j])
                    k=k+1
                else:
                    newsVectorData.append(0)
                j=j+1
            if(sum(newsVectorData)>weightLimit):
                newsInfoList.append(newsInfo(newsId=newsId,newsVector=newsVectorData))
        return newsInfoList
    @staticmethod
    def getIDF(keywordList, valueList):
        totalCount = sum(valueList)
        print("total count:" + str(totalCount))
        IDFList = list()
        alpha = 1
        for i in range(len(valueList)):
            IDFList.append(math.log(totalCount / (valueList[i] + alpha)))
        return IDFList
#         for news in self.newsList:
#             pass
#         pass
    
    
        
    
        
