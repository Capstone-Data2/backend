import pandas as pd
from pymongo import MongoClient
from sklearn.linear_model import LogisticRegression
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
    modelfile = f'models/{rank}/pos{position}_win.sav'
    joblib.dump(logreg, modelfile)


#Example line to generate a model
#posModel('crusader', 1)
