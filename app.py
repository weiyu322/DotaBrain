# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 23:22:34 2016

@author: Administrator
"""

from flask import Flask
from flask import jsonify
from recommendation.Engine import Engine
from recommendation.Utils import loadHeroDict
from recommendation.BaseModel import BaseModel

app = Flask(__name__)


@app.route('/api/v1.0/recommendation')
def recommend():
    
    return jsonify()

if __name__ == '__main__':
    modelPath = "resource/model.pkl"    
    heroDict = loadHeroDict("resource/heroes.json")
    baseModel = BaseModel(modelPath,heroDict)
    
    app.run()