import pandas as pd
from pymongo import MongoClient
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn import preprocessing
import joblib

#Getting specific features to look at depending on the rank
from positionFeatures import posfeatures

matchPlayers =  'matches_players'
client = MongoClient("mongodb+srv://testadmin:testadmin@dbtest.37wj1.mongodb.net/dbtest?retryWrites=true&w=majority")
db = client.dota2

def posModel(rank, position):
    rankCollection= db[rank + matchPlayers]
    collection = rankCollection.find({'ml_lane_role': position, }, {'_id':0})
    df = pd.DataFrame(list(collection))
    y = df['win']
    x = df[posfeatures(position)].values
    
    #Creation of model
    logreg = LogisticRegression(random_state=0, max_iter=1000).fit(x, y)
    #Saving the model
    modelfile = f'backend/data2/model/models/{rank}/pos{position}_win.sav'
    joblib.dump(logreg, modelfile)

def coreModels(rank):
    rankCollection= db[rank + matchPlayers]
    collection = rankCollection.find({}, {'last_hits': 1, 'obs_placed': 1, 'gpm': 1, '_id': 0})
    df = pd.DataFrame(list(collection))
    X = df[['last_hits', 'obs_placed', 'gpm']]

    min_max_scaler = preprocessing.MinMaxScaler()
    scaler_model = min_max_scaler.fit(X.values)

    X_train_minmax = scaler_model.transform(X.values)

    kmeans = KMeans(n_clusters=2)

    y = kmeans.fit(X_train_minmax)

    modelfile = f'models/{rank}/core_model.sav'
    scalerfile = f'models/{rank}/core_scaler.sav'
    joblib.dump(y, modelfile)
    joblib.dump(scaler_model, scalerfile)


#Example line to generate a model
#posModel('archon', 1)
#coreModels('legend')
