from flask import request
from flask_restful import Resource

import pandas as pd
import numpy as np
from IPython.display import display
from pandas_profiling import ProfileReport

import pickle

from sklearn.cluster import DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.cluster import MeanShift

import time

def saveModel(modelClass, fileName):
	fileName+='.sav'
	pickle.dump(modelClass, open('models/'+fileName, 'wb'))
	return 'models/'+fileName

def loadModel(fileName):
	model = pickle.load(open(fileName, 'rb'))
	return model

def getSongsFromQuery(name, album,  Artist):
    totalSongs = len(album)
    sampleDf = pd.DataFrame(columns = df.columns)
    featureSpace = pd.DataFrame(columns = column2Cluster)
    for i in range(totalSongs):
        f1 = df['name']==name[i]
        f2 = df['album']==album[i]
        temp = df.loc[f1&f2]
        if len(temp) == 1:
            featureSpace = pd.concat([featureSpace, temp[column2Cluster]], ignore_index = True)
            sampleDf = pd.concat([sampleDf, temp], ignore_index = False)
        else:
            f3 = df['artist']==Artist[i]
            temp = temp.loc[f3]
            featureSpace = pd.concat([featureSpace, temp[column2Cluster]], ignore_index = True)
            sampleDf = pd.concat([sampleDf, temp], ignore_index = False)
    return featureSpace.values, sampleDf
def findNumberCluster(x):
    ms = MeanShift(bandwidth=5).fit(x)
    # print(ms.predict(x))
    return len(np.unique(ms.fit_predict(x)))

def naivePlaylist(sampleNoClusters, x):
    sampleGmm = GaussianMixture(n_components = sampleNoClusters).fit(x)
    probabilities = sampleGmm.predict_proba(x)
    gmm_labels = sampleGmm.predict(x)
    finalPlaylist = []
    
    for _ in range(sampleNoClusters):
        finalPlaylist.append([])
        
    for i in range(len(x)):  
        for j in range(sampleNoClusters):
            if probabilities[i][j]>=1/sampleNoClusters:
                finalPlaylist[j].append(i)
#                 print("I: ", i)
#         print(finalPlaylist)
    return finalPlaylist

def playLsit2Song(toChoose, finalPlaylist):
    toRet = []
    for i in range(len(finalPlaylist)):
        toRet.append([])
        for j in range(len(finalPlaylist[i])):
            list(toChoose.iloc[finalPlaylist[i][j],:][['name', 'album', 'artist']])
            toRet[-1].append(list(toChoose.iloc[finalPlaylist[i][j],:][['name', 'album', 'artist']]))
    return toRet


def extrapolation(finalPlaylist, maxSongsPerPlaylist, localSongsData, songsPlayList): 
    for playlistNo in range(len(finalPlaylist)):
        if len(finalPlaylist[playlistNo])>=maxSongsPerPlaylist:
            continue
        currentSongs = len(finalPlaylist[playlistNo])
        moreSongsReq = maxSongsPerPlaylist - currentSongs
        newSongsPerCS = moreSongsReq/currentSongs
        
        predictions = gmmUni.predict(localSongsData[finalPlaylist[playlistNo]]) ## A prediction for each plalist
        
        countOfPrediction = {i: len(predictions[predictions==i]) for i in np.unique(predictions)}
        songs = []
        tupples = []
        s1 = len(finalPlaylist[playlistNo])
        forPlaylist = [] 
        for i in range(len(np.unique(predictions))): 
            temp = clusters[predictions[i]][column2Cluster].values - localSongsData[finalPlaylist[playlistNo]][i]
    
            temp = np.linalg.norm(temp,axis = 1)
            sortedArg = np.argsort(temp)[:moreSongsReq]
            indices = np.random.choice(sortedArg,
            1+int(moreSongsReq*countOfPrediction[predictions[i]]/len(predictions)))
            songsPlayList[playlistNo]+=clusters[predictions[i]].iloc[indices,:][['name', 'album', 'artist']].values.tolist()
            s1+=len(indices)
    return songsPlayList

df = pd.read_csv('a0_650.csv')
df.drop(["Unnamed: 0", "Unnamed: 0.1"], axis = 1, inplace = True)
column2Cluster = ['danceability', 'energy', 'liveness' , 'tempo', 'valence']
df2Cluster = df[column2Cluster]
#df2Cluster.shape

#Importing model
dbscan = loadModel('models/dbscanForCluster.sav')
gmmUni = loadModel('models/GMM.sav')

uniLabels = np.unique(dbscan.labels_)
labels = dbscan.labels_
noClusters = len(uniLabels)-1

X = df2Cluster.values

pro = gmmUni.predict_proba(X)

newCols = ['album', 'name', 'artist']
futureDf = {i: df[i].values for i in newCols}
for i in range(noClusters):
    futureDf['Cluster'+str(i)] = 0
futureDf['maxClass'] =  0
futureDf['sumProbabs'] = 0

for i in range(noClusters): 
    futureDf['Cluster'+str(i)] = pro[:, i]
futureDf['maxClass'] = np.argmax(pro, axis = 1)
futureDf['sum'] = np.sum(pro, axis = 1)
futureDf = pd.DataFrame(futureDf)

## Data preprocessing starts from here: 
clusters = []
for i in range(noClusters):
    clusters.append(pd.read_csv('savedData/Clustered_Songs/Cluster'+str(i)+'.csv'))

class PlaylistsResource(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No song data provided'}, 400
        
        # Below format is stored in: (album, name, artist)
        newSongs = json_data["songs"]
        maxSongsPerPlaylist = json_data["maxSongsPerPlaylist"]

        newSongs = np.array(newSongs)
        #t1 = time.time()

        x,g = getSongsFromQuery(newSongs[:,1], newSongs[:,0], newSongs[:,2])
        noSampleClusters = findNumberCluster(x)
        clusteredPlaylist = naivePlaylist(noSampleClusters, x)

        s = playLsit2Song(g, clusteredPlaylist)
        s = extrapolation(clusteredPlaylist, maxSongsPerPlaylist, x, s)

        if not s:
            return {'message': 'Error in generating Playlist'}, 401

        #print(time.time() - t1)
        return {'playlists_number': noSampleClusters, 'data': s}, 200