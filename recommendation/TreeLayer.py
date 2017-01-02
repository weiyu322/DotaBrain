# -*- coding: utf-8 -*-
"""
Created on Sun Jan 01 20:08:54 2017

@author: Administrator
"""

class TreeLayer:
    """
    montecarlo tree的一层
    """
    
    side = 1
    remainList = []
    nodeSet = []
    playedTimes = 0         #这一局面下所有可选策略总的实验次数
    
    
    def __init__(self,remainList):
        self.remainList = remainList
    
    def add(self,node):
        """
        往这一层中添加节点
        """
        self.nodeSet.append(node)



class Node:

    ucbScore = 0
    playedTimes = 0
    winTimes = 0
    nextLayer = None
    heroId = None
        
    def __init__(self,heroId,nextLayer=None):
        self.heroId = heroId
        self.nextLayer = nextLayer
    
    def winRate(self):
        return self.winTimes / self.playedTimes
    
    def ucbScore(self,totalPlayedTimes):
        """
        UCB1 algorithm
        """
        winRate = self.winRate()
        confidenceInterval = 
        return self.winTimes / self.playedTimes + 
    
def ucbScore():
    pass

    