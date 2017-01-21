# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 23:22:34 2016

@author: Administrator
"""

from flask import Flask,request
from flask import jsonify
from recommendation.Engine import Engine
from recommendation.Utils import loadHeroDict
from recommendation.BaseModel import BaseModel

app = Flask(__name__)


@app.route('/api/v1.0/recommend',methods=["POST"])
def recommend():
    
    ownSide = request.json["ownSide"]
    print ownSide

    enemySide = request.json["enemySide"]
    topK = request.json["topK"]

    ownSide = map(lambda x:heroList[x],ownSide)
    enemySide = map(lambda x:heroList[x],enemySide)
    recommendInfo = engine.recommend(ownSide,enemySide,topK)
    
    recommendInfo["recommendation"] = map(lambda x:heroList[x],
                                            recommendInfo["recommendation"])
    print recommendInfo
    
    return jsonify(recommendInfo)

@app.route("/api/v1.0/predict",methods=["POST"])
def predict():  
    
    radiant = request.json["radiant"]
    dire = request.json["dire"]
    radiant = map(lambda x:heroList[x],radiant)
    dire = map(lambda x:heroList[x],dire)
    result = baseModel.predictProba(radiant,dire)
    response = {"radiantWinRate":result[0],
                "direWinRate":result[1]}
    
    return jsonify(response)
        
if __name__ == '__main__':
    modelPath = "resource/model.pkl"    
    heroDict,heroList = loadHeroDict("resource/heroes.json")
    heroList = dict((v,k) for k,v in heroList.iteritems()) 
    baseModel = BaseModel(modelPath,heroDict)
    engine = Engine(baseModel,heroDict,method="MCTS")
    app.run()