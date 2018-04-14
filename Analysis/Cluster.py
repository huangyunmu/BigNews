'''


@author: andyh
'''
import numpy as np
class Cluster(object):
    '''
    classdocs
    '''

    def __init__(self, newsVectorList):
        
        '''
        Constructor
        '''
        self.newsVectorList = newsVectorList
    @staticmethod
    def computeKMeansCost():
        return 0

    def getKMeansResult(self, k=20, iteration=100):
        """
        Using naive k-means
        """
        n = self.newsVectorList[0].newsVector.shape[0]
        centerList = list()
#         compute the initial center
        randomOrderList = np.arange(n)  
        np.random.shuffle(randomOrderList)  # permutation
        
        for i in range(k):
            centerList.append(self.newsVectorList[randomOrderList[i]].newsVector)
        
        assignementList = list()
        for i in range(k):
            assignementList.append(list())
       
        for iter in range(iteration):
            # assignment
            for item in self.newsVectorList:
                vector = item.newsVector
                maxSimi = 0
                maxIndex = 0
                for i in range(k):
                    simi = Cluster.getCosSimi(vector, centerList[i])
                    if(simi > maxSimi):
                        maxSimi = simi
                        maxIndex = i
                assignementList[maxIndex].append(item)
            # update
            for i in range(k):
                if len(assignementList[i]) == 0:
                    continue
                result = np.zeros(assignementList[i][0].newsVector.shape[0])
                for j in range(len(assignementList[i])):
                    result = result + assignementList[i][j].newsVector
                result = result / len(assignementList[i])
                centerList[i] = result
            # clear the assignment list
            if(iter != iteration - 1):
                for i in range(k):
                    assignementList[i][:] = []
        cost = self.computeKMeansCost()
        return centerList, assignementList, cost
    def getHierResult(self, k=20, mergeLimit=0.8):
        l = len(self.newsVectorList)
#         l=25
        vectorDistanceStrategy="Cos"
        maxSimilarity = 0
        indexI = -1
        indexJ = -1
        similarityMatrix = np.zeros((l, l))
#         Test
#         for i in range(l):
#             for j in range(i):
#                 similarityMatrix[i][j] = (i + j)/10
#                 similarityMatrix[j][i] = (i + j)/10
        newsMergedList=list()
        
        for i in range(l):
#             Test
#             newsMergedList.append([i])
            newsMergedList.append([self.newsVectorList[i].newsId])
        
        for i in range(l):
                for j in range(i):
                    similarityMatrix[i][j]=Cluster.getVectorSimilarity(self.newsVectorList[i].newsVector, self.newsVectorList[j].newsVector,strategy=vectorDistanceStrategy)
                    similarityMatrix[j][i]=similarityMatrix[i][j]
#                     if(similarityMatrix[i][j]<limit):
# #                         print("<limit")
#                         similarityMatrix[i][j]=0
#                         similarityMatrix[j][i]=0
                    if(similarityMatrix[i][j] > maxSimilarity):
                        maxSimilarity = similarityMatrix[i][j]
                        indexI = i
                        indexJ = j
#         print(similarityMatrix)
#         for item in newsMergedList:
#             print(item)
        while(True):
            # merge two closest point
            if(indexI == -1):
                break
            if(maxSimilarity<mergeLimit):
                break
#             print("max similarity:"+str(maxSimilarity))
            simiVectorI = similarityMatrix[indexI]
            simiVectorJ = similarityMatrix[indexJ]
            # delete data in index i and index j
            simiVectorI = np.delete(simiVectorI, indexI, 0)
            simiVectorI = np.delete(simiVectorI, indexJ, 0)
            simiVectorJ = np.delete(simiVectorJ, indexI, 0)
            simiVectorJ = np.delete(simiVectorJ, indexJ, 0)
            newSimiVector = simiVectorI
            for index in range(l - 2):
                if(simiVectorI[index] > simiVectorJ[index]):
                    newSimiVector[index] = simiVectorJ[index]
            
            similarityMatrix = np.delete(similarityMatrix, indexI, 0)
            similarityMatrix = np.delete(similarityMatrix, indexI, 1)
            similarityMatrix = np.delete(similarityMatrix, indexJ, 0)
            similarityMatrix = np.delete(similarityMatrix, indexJ, 1)
            similarityMatrix=np.row_stack((similarityMatrix, newSimiVector))
            newSimiVector=np.append(newSimiVector, 0)
            similarityMatrix=np.column_stack((similarityMatrix, newSimiVector))
            tempNewIDList=newsMergedList[indexI]+newsMergedList[indexJ]
            
            newsMergedList.pop(indexI)
            newsMergedList.pop(indexJ)
            newsMergedList.append(tempNewIDList)
#             print(similarityMatrix)
#             print(newsMergedList)
            #update l
            l=similarityMatrix.shape[0]
#             print("Shape:"+str(l))
            #find the update for next round
            maxSimilarity=0
            indexI=-1
            indexJ=-1
            for i in range(l):
                for j in range(i):
                    if(similarityMatrix[i][j] > maxSimilarity):
                        maxSimilarity = similarityMatrix[i][j]
                        indexI = i
                        indexJ = j
#             print(similarityMatrix)
#             for item in newsMergedList:
#                 print(item)
        #only the real cluster(size>1) will be return
        newsMergedList=list(filter(lambda x:len(x)>1,newsMergedList))
        #Sort the newsMergedList
        for i in range(len(newsMergedList)):
            for j in range(i):
                if(len(newsMergedList[i])>len(newsMergedList[j])):
                    temp=newsMergedList[i]
                    newsMergedList[i]=newsMergedList[j]
                    newsMergedList[j]=temp
        return newsMergedList
    @staticmethod
    def getVectorSimilarity(vector1,vector2,strategy="Cos"):
        #cos similarity
        similarity=0
        if(strategy=="Cos"):
            similarity = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * (np.linalg.norm(vector2)))
        #Jaccard similarity
        if(strategy=="Jac"):
            l=len(vector1)
            countOr=0
            countAnd=0
            for i in range(l):
                if(vector1[i]>0 or vector2[i]>0):
                    countOr=countOr+1
                if(vector1[i]>0 and vector2[i]>0):
                    countAnd=countAnd+1
            similarity=countAnd/countOr
        return  similarity
        
