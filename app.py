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
    
    ownSide = request.form["ownSide"]
    print ownSide
    print eval(ownSide)
    enemySide = request.form["enemySide"]
    topK = request.form["topK"]
    #print list(ownSide)
    
    #urllib.encode传过来的数据是unicode字符串形式，先解析成int型list
    """
    ownSide = ownSide.split(",")
    
    print ownSide
    ownSide = list(ownSide)
    print ownSide
    del ownSide[0]
    del ownSide[len(ownSide)-1]

    print ownSide
    ownSide = map(int,ownSide)
    
    enemySide = enemySide.split(",")
    enemySide = list(enemySide)
    del enemySide[0]
    del enemySide[len(enemySide)-1]
    enemySide = map(int,enemySide)
    
    print ownSide
    """
    ownSide = eval(ownSide)
    enemySide = eval(enemySide)
    
    recommendInfo = engine.recommend(ownSide,enemySide)
    print recommendInfo
    
    return jsonify(recommendInfo)

@app.route("/api/v1.0/predict",methods=["POST"])
def predict():  
    
    radiant = request.form["radiant"]
    dire = request.form["dire"]
        
if __name__ == '__main__':
    modelPath = "resource/model.pkl"    
    heroDict = loadHeroDict("resource/heroes.json")
    baseModel = BaseModel(modelPath,heroDict)
    engine = Engine(baseModel,heroDict,method="PureMC",epochs=100)
    app.run()