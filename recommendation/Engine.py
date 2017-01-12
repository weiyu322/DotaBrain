# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 16:13:08 2016

@author: Administrator
"""
from PureMC import PureMC
from MCTS import MCTS
from BaseModel import BaseModel
from Utils import loadHeroDict
from time import time

class Engine:
    """
    英雄推荐引擎
    """
    
    heroDict = {}
    epochs = 0
    baseModel = None
    method = ""
    
    def __init__(self,baseModel,heroDict,method="PureMC",epochs=100):
        
        self.baseModel = baseModel
        self.heroDict = heroDict        
        self.epochs = epochs
        self.method = method
    
    def recommend(self,ownSide,enemySide,topK=3):
        """
        返回topK个推荐英雄
        """
        if topK < 1:
            print "英雄推荐数至少为1"
            return
            
        recommendInfo = {}
        if self.method == "PureMC":
            searchModel = PureMC(ownSide,enemySide,
                                 self.baseModel,self.heroDict)            
            searchModel.run(epochs=self.epochs)
            recommendInfo["avgWinRate"] = searchModel.getAvgWinRate()
            heroList = searchModel.policy()
            recommendInfo["recommendation"] = heroList[0:topK]
            
            return recommendInfo
        else:
            """
            method == "MCTS"
            """
            searchModel = MCTS(ownSide,enemySide,
                               self.baseModel,self.heroDict)
            searchModel.run(runTime=5)
            recommendInfo["avgWinRate"] = searchModel.getAvgWinRate()
            heroList = searchModel.policy()
            recommendInfo["recommendation"] = heroList[0:topK]
            
            return recommendInfo
        
        
        
if __name__ == "__main__":
    
    modelPath = "../resource/model.pkl"    
    heroDict = loadHeroDict("../resource/heroes.json")
    baseModel = BaseModel(modelPath,heroDict)
    ownSide = [6,7,8,9]
    enemySide = [1,2,3,4]
    
    engine = Engine(baseModel,heroDict,epochs=100,method="MCTS")
    
    start = time()
    recommendInfo = engine.recommend(ownSide,enemySide)
    end = time()
    print "total time: %f s" % (end - start)