import pandas as pd
import config as cfg
import numpy as np
from itertools import *
from math import sqrt
from scipy.sparse import coo_matrix, csr_matrix

# Loading the dataset in the dataframe
data = pd.read_csv('./data/the-movies-dataset/ratings_small.csv')
data = data.head(500)

# Specifying values of k(nearest neighbours)
k = cfg.variables['k']

#creating sparse matrices
ratings = coo_matrix((data['rating'], (data['userId'], data['movieId'])))
ratingsCsr = ratings.tocsr()
# calculating the count(in this dataset the ids are autoincremented from 1, so max id is count)
userCount = max(data['userId'])
#creating the similarity matrix - sim

def getCommonRatings(user1, user2):
    ratingList1 = []
    ratingList2 = []
    for movie in ratingsCsr[user1].indices:
        if movie in ratingsCsr[user2].indices:
            ratingList1.append(ratingsCsr[user1].data[[ratingIndex1 for ratingIndex1,j in zip(count(), ratingsCsr[user1].indices) if j == movie][0]])
            ratingList2.append(ratingsCsr[user2].data[[ratingIndex2 for ratingIndex2,j in zip(count(), ratingsCsr[user2].indices) if j == movie][0]])
    return ratingList1, ratingList2

def cosineSimilarity(ratingList1, ratingList2):
    if len(ratingList1)>0 and len(ratingList2)>0:
        return sum([a*b for a,b in zip(ratingList1, ratingList2)])/sqrt(sum([i*i for i in ratingList1])*sum([i*i for i in ratingList2]))
    else:
        return 0

def getSimilarityMatrix():
    sim = np.empty(shape=(userCount+1, userCount+1))
    # sim = []
    userList = np.unique(ratings.row)
    for user1 in userList:
        for user2 in userList:
            if user1 is not user2:
                sim[user1][user2] = cosineSimilarity(*getCommonRatings(user1, user2))
            else:
                sim[user1][user1] = 1
    return sim

print(getSimilarityMatrix())
