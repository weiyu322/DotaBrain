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
    """
    side = True             #1表示enemyside，0表示ownside
    remainList = []         #本层可选英雄集合
    heroToBeSelected = []   #本层还未选择过得英雄
    nodeSet = []            #本层节点集合
    playedTimes = 0         #这一局面下所有可选策略总的实验次数
    parentNode = None
    """
    
    def __init__(self,remainList,side):
        self.remainList = remainList
        self.heroToBeSelected = list(remainList)
        self.side = side
        self.nodeSet = []
        self.playedTimes = 0
        self.parentNode = None
        #self.parentNode = parentNode
        
        
    def add(self,node):
        """
        往这一层中添加节点
        """
        if node.getHeroId() in self.heroToBeSelected:
            self.nodeSet.append(node)
            self.heroToBeSelected.remove(node.getHeroId())
            
        else:
            return
        
        return
    
    def length(self):
        
        return len(self.nodeSet)

    def getNodeByInd(self,i):
        
        if self.length() == 0:
            return None
        
        return self.nodeSet[i]
    
    def winRate(self):
        """
        计算本层节点的总胜率
        """
        totalWinRate = 0
        for node in self.nodeSet:
            totalWinRate += node.winRate()
        
        return totalWinRate / self.length()
    
    def getBestNode(self):
        """
        返回ucb值最大的节点
        """
        node = self.nodeSet[0]
        score = node.ucbScore(self.playedTimes)
        for i in self.nodeSet:
            if i.ucbScore(self.playedTimes) > score:
                node = i
                score = node.ucbScore(playedTimes)
        
        return node
    
    def avgWinRate(self):
        totalWinRate = 0
        for node in self.nodeSet:
            totalWinRate += node.totalWinRate
        
        return totalWinRate / self.playedTimes
    
    def heroDict(self):
        heroes = {}
        for node in self.nodeSet:
            heroes[node.heroId] = node.playedTimes
        
        return heroes
        
    def sortByPlayedTimes(self):
        heroes = self.heroDict()
        sortedList = sorted(heroes.iteritems(), 
                                key=lambda d:d[1], reverse = True)
        return sortedList
        
class Node:
    """
    #ucbScore = 0
    playedTimes = 0
    totalWinRate = 0
    nextLayer = None
    heroId = None
    """
    
    def __init__(self,heroId,nextLayer=None):
        self.heroId = heroId
        self.nextLayer = nextLayer
        self.playedTimes = 0
        self.totalWinRate = 0
    
    def setNextLayer(self,layer):
        
        self.nextLayer = layer
        
    def winRate(self):

        return self.totalWinRate / self.playedTimes
    
    def ucbScore(self,totalPlayedTimes):
        """
        UCB1 algorithm
        ucb1 = winrate + sqrt(2*lnn / ni)
        """
        winRate = self.winRate()
        #print totalPlayedTimes
        #print self.playedTimes
        confidenceInterval = math.sqrt(2 * math.log(totalPlayedTimes,math.e) / self.playedTimes)
        
        return winRate + confidenceInterval 
    
    
    def getHeroId(self):
        
        return self.heroId
    
    def __str__(self):
        dic = {"heroId":self.heroId,
               "playedTimes":self.playedTimes}
        return str(dic)
        
def ucbScore():
    pass

    