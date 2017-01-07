# -*- coding: utf-8 -*-
"""
Created on Sun Jan 01 20:08:54 2017

@author: Administrator
"""
import math

class TreeLayer:
    """
    montecarlo tree的一层
    """
    
    side = 0                #1表示enemyside，0表示ownside
    remainList = []         #本层可选英雄集合
    nodeSet = []
    playedTimes = 0         #这一局面下所有可选策略总的实验次数
    parentNode = None
    
    def __init__(self,remainList,side,parentNode):
        self.remainList = remainList
        self.side = side
        self.parentNode = parentNode
        
    def add(self,node):
        """
        往这一层中添加节点
        """
        self.nodeSet.append(node)
    
    def length(self):
        
        return len(self.nodeSet)

    def getNodeByInd(self,i):
        
        if self.length() == 0:
            return None
        
        return self.nodeSet[i]

class Node:

    ucbScore = 0
    playedTimes = 0
    winTimes = 0
    nextLayer = None
    heroId = None
        
    def __init__(self,heroId,nextLayer=None):
        self.heroId = heroId
        self.nextLayer = nextLayer
    
    def setNextLayer(self,layer):
        
        self.nextLayer = layer
        
    def winRate(self):

        return self.winTimes / self.playedTimes
    
    def ucbScore(self,totalPlayedTimes):
        """
        UCB1 algorithm
        ucb1 = winrate + sqrt(2*lnn / ni)
        """
        winRate = self.winRate()
        confidenceInterval = math.sqrt(2 * math.log(totalPlayedTimes) / self.playedTimes)
        
        return winRate + confidenceInterval 
    
    def getUcbScore(self):
        
        return self.ucbScore
        
def ucbScore():
    pass

    