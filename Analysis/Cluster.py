'''


@author: andyh
'''
import numpy as np
from sklearn.cluster import KMeans
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
    def getHierResult(self, k=20, limit=0.8):
        l = len(self.newsVectorList)
#         l=25
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
                for j in range(i+1):
                    similarityMatrix[i][j]=Cluster.getCosSimi(self.newsVectorList[i].newsVector, self.newsVectorList[j].newsVector)
                    similarityMatrix[j][i]=similarityMatrix[i][j]
#                     if(similarityMatrix[i][j]<limit):
# #                         print("<limit")
#                         similarityMatrix[i][j]=0
#                         similarityMatrix[j][i]=0
                    if(i!=j and similarityMatrix[i][j] > maxSimilarity):
                        maxSimilarity = similarityMatrix[i][j]
                        indexI = i
                        indexJ = j
        print(similarityMatrix)
        while(True):
            # merge two closest point
            if(indexI == -1):
                break
            if(maxSimilarity<limit):
                break
#             print(maxSimilarity)
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
            tempNewIDList=newsMergedList[indexI]
            newsMergedList[indexJ]=newsMergedList[indexJ]+tempNewIDList
            newsMergedList.pop(indexI)
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
        return newsMergedList
        
    def getKMeansPlusResult(self, k=20):
        """
        using sklearn.cluster k-means++
        """
        pass
        estimator = KMeans(n_clusters=k)
    
    @staticmethod
    def getCosSimi(vector1, vector2):
        similarity = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * (np.linalg.norm(vector2)))
        return similarity
        
        
