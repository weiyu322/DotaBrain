# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 22:44:48 2016

@author: Administrator
"""


def loadHeroDict(path):
    """
    读取官方的heroes.json映射为连续编码的heroDict
    """
    import json
    
    f = open(path)
    heroes = json.load(f)
    f.close()
    heroes = heroes["heroes"]
    herolist = {}
    for i in heroes:
        herolist[i["id"]] = i["localized_name"]
    newheroid = {}
    count = 0
    for i in herolist:
        newheroid[i] = count
        count += 1
        
    return newheroid,herolist


def toFeatureVector(radiant,dire,heroDict):
    """
    将双方阵容list转换为特征向量
    前heroNum维为radiant特征，后heroNum维为dire特征
    radiant ： 天辉阵容list
    dire ： 夜魇阵容list
    由于英雄编码不是连续编码的，所以通过heroDict将原始编码应映射为连续编码
    """
    featureVector = [0] * len(heroDict) * 2
    for i in radiant:
        featureVector[heroDict[i]] = 1
    for i in dire:
        featureVector[heroDict[i]+len(heroDict)] = 1
    
    return featureVector

def loadPickle(modelPath):
    """
    反序列化模型对象
    """
    import pickle
    
    pklFile = open(modelPath,"rb")
    model = pickle.load(pklFile)
    pklFile.close()
    
    return model 
