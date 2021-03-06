# coding:utf-8
'''

@author: andyh
'''
import json
import math
import numpy as np
def sortKeyword(keywordList, valueList, strategy="ByKeyword"):
        """
        To be updated
        """
        for i in range(len(keywordList)):
            for j in range(0, i):
                if((strategy == "ByValue" and valueList[i] > valueList[j])or(strategy == "ByKeyword" and keywordList[i] < keywordList[j])):
                    temp = keywordList[i]
                    keywordList[i] = keywordList[j]
                    keywordList[j] = temp
                    temp = valueList[i]
                    valueList[i] = valueList[j]
                    valueList[j] = temp
class news(object):
    def __init__(self, title, jump, content,keywords, values):
        self.title = title
        self.jump = jump
        self.content=content
        self.keywordList = keywords
        self.valueList = values
        sortKeyword(self.keywordList, self.valueList, strategy="ByKeyword")
    
        
    def toString(self):
        result = ""
        result = result + "title:" + self.title + "\n"
        result = result + "jump:" + self.jump + "\n"
        result = result + "content(first 100):"+self.content[:100]+"\n"
        for i in range(len(self.keywordList)):
            result = result + str(self.keywordList[i]) + " " + str(self.valueList[i]) + ","
        result = result + "\n"
        return result
    def toDict(self):
        result=dict()
        result["title"]=self.title
        result["jump"]=self.jump
        result["content"]=self.content
        return result
class newsInfo(object):
    def __init__(self, newsId, newsVector):
        self.newsId = newsId
#         self.newsVector = np.array(newsVector)
        self.newsVector = newsVector
    def toString(self):
        result = ""
        result = result + "newsId:" + str(self.newsId) + "\n"
        l = self.newsVector.shape[0]
        for i in range(l):
            result = result + str(self.newsVector[i]) + " "
        result = result + "\n"
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
            if(len(keywords) == 0):
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
                currentNewsList.append(news(title=item["title"], jump=item["jump"],content=item["content"],keywords=keywordList, values=valueList))
        self.newsList = self.newsList + currentNewsList
        self.updateKeywordDict(currentNewsList)
    def printAllNews(self, filename=None):
        for news in self.newsList:
            if(filename == None):
                print(news.toString())
    def getAllNews(self):
        return self.newsList
    def updateKeywordDict(self, currentNewsList):
        strategy = 1
        # for each keyword it will be counted as its frequency
        if(strategy == 0):
            for news in currentNewsList:
                l = len(news.keywordList)
                for i in range(l):
                    keyword = news.keywordList[i]
                    if(keyword in self.keywordDict):
                        self.keywordDict[keyword] = self.keywordDict[keyword] + news.valueList[i]
                    else:
                        self.keywordDict[keyword] = news.valueList[i]    
        # for each keyword it will be only count once
        if(strategy == 1):
            for news in currentNewsList:
                l = len(news.keywordList)
                for i in range(l):
                    keyword = news.keywordList[i]
                    if(keyword in self.keywordDict):
                        self.keywordDict[keyword] = self.keywordDict[keyword] + 1
                    else:
                        self.keywordDict[keyword] = 1
    def getKeyWordDict(self):
        return self.keywordDict  
#     def getTopKKeywordDict(self, vectorSize=100):
#         result = dict()
# #         if(vectorSize == 0):
# #             vectorSize = self.vectorSize
#         tempResult = sorted(self.keywordDict.values(), reverse=True)
#         if(vectorSize < len(tempResult) - 1):
#             vectorSize = len(tempResult) - 1
#         limit = tempResult[vectorSize]
# #         print(limit)
#         for key, value in  self.keywordDict.items():
#             if(value > limit):
#                 result[key] = value
#         return result, vectorSize
        
    def getTopKKeywordList(self, vectorSize=100):
        keywordList, valueList = self.getSortedKeywordListByValue()
        l = len(keywordList)
        if(vectorSize > l):
            vectorSize = l
        keywordList = keywordList[0:vectorSize]
        valueList = valueList[0:vectorSize]
        return keywordList, valueList
    @staticmethod
    def loadData(filename):
        with open(filename) as f:
            json_str = f.read()
            data = json.loads(json_str)
        return data
    def getSortedKeywordListByValue(self):
        keywordList = list()
        valueList = list()
        for key, value in self.keywordDict.items():
            keywordList.append(key)
            valueList.append(value)
        sortKeyword(keywordList, valueList, strategy="ByValue")
        return keywordList, valueList
    
    def vectorLization(self, vectorSize=20, weightLimit=0.8):
        keywordList, valueList = self.getTopKKeywordList(vectorSize)
#         print("ByValue")
#         print(keywordList)
        sortKeyword(keywordList, valueList, strategy="ByKeyword")
#         print("ByKeyword")
#         print(keywordList)


        documentNum = len(self.newsList)
        IDFList = Worker.getIDF(documentNum, keywordList, valueList)
#         print("len IDF")
#         print(len(IDFList))
        newsInfoList = list()
        for i in range(len(self.newsList)):
            news = self.newsList[i]
            newsKeywordList = news.keywordList
            newsValueList = news.valueList
#             newsVectorData=list()
            newsVectorData = np.zeros(vectorSize)
            j = 0
#             print(newsKeywordList)
            while(j < vectorSize):
                isFound = False
                for k in range(len(newsKeywordList)):
                    if(newsKeywordList[k] == keywordList[j]):
#                         print(newsKeywordList[k],keywordList[j])
                        isFound = True
                        break
                if(isFound):
#                     newsVectorData.append(newsValueList[k]*IDFList[j])
                    newsVectorData[j] = newsValueList[k] * IDFList[j]
                else:  
#                     newsVectorData.append(0)
                    pass  
                j = j + 1
            if(sum(newsVectorData) > weightLimit):
                newsId = i
                newsInfoList.append(newsInfo(newsId=newsId, newsVector=newsVectorData))
                
            else:
#                 print("Delete news")
                pass
        return newsInfoList
    @staticmethod
    def getIDF_Old(keywordList, valueList):
        totalCount = sum(valueList)
        print("total count:" + str(totalCount))
        IDFList = list()
        alpha = 1
        for i in range(len(valueList)):
            IDFList.append(math.log(totalCount / (valueList[i] + alpha)))
        return IDFList
    @staticmethod
    def getIDF(documentNum, keywordList, valueList):
        """
        To be implemented 
        """
        print("total totalDocument:" + str(documentNum))
        IDFList = list()
        alpha = 0
        for i in range(len(valueList)):
            IDFList.append(math.log(documentNum / (valueList[i] + alpha)))
        return IDFList
#         for news in self.newsList:
#             pass
#         pass
    
    
        
    
        
