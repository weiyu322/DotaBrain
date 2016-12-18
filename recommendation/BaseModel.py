# -*- coding: utf-8 -*-

from Utils import toFeatureVector
import numpy as np
import pickle

class BaseModel:
    """
    封装英雄预测模型类
    """
    model = None
    heroDict = {}
    
    def __init__(self,modelPath,heroDict):
        
        f = open(modelPath,"rb")
        model = pickle.load(f)
        self.model = model
        self.heroDict = heroDict
    
    def predict(self,radiant,dire):
        """
        预测胜负结果
        radiant胜：1
        dire胜：0
        """
        featureVector = toFeatureVector(radiant,dire,self.heroDict)
        """
        Passing 1d arrays as data is deprecated in 0.17 
        and willraise ValueError in 0.19. Reshape your 
        data either using X.reshape(-1, 1) if your data 
        has a single feature or X.reshape(1, -1) if it 
        contains a single sample.
        """
        featureVector = np.array(featureVector).reshape(1,-1)
        
        return self.model.predict(featureVector)[0]
    
    def predictProba(self,radiant,dire):
        """
        预测胜率,返回一个二维array，array[0] -> radiant胜率
        """
        featureVector = toFeatureVector(radiant,dire,self.heroDict)   
        featureVector = np.array(featureVector).reshape(1,-1)
        
        return self.model.predict_proba(featureVector)[0]
                   