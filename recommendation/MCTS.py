# -*- coding: utf-8 -*-
"""
Created on Sun Jan 01 17:54:48 2017

@author: Administrator
"""
import random
from TreeLayer import TreeLayer,Node

class MCTS:
    """
    基于MonteCarlo Tree Search的搜索算法
    """
    
    ownSide = []
    enemySide = []
    heroDict = {}
    remainList = []
    model = None
    heroWinRate = {}        #记录英雄胜率
    avgWinRate = 0          #当前局面下平均胜率

    def __init__(self,ownSide,enemySide,model,heroDict):
        
        if not self.isLegalInput(ownSide,enemySide,heroDict):
            return 

        self.ownSide = ownSide
        self.enemySide = enemySide
        self.heroDict = heroDict
        #remaining从hero全集中剔除双方已选择的英雄
        self.remainList = list(set(self.heroDict).difference(set(self.ownSide)
                                .union(set(self.enemySide))))
        self.model = model
    
    def run(self):
        
        """
        如果己方已选4个，对方选了5个，则只需要遍历候选英雄集
        """
        if len(self.ownSide) == 4 and len(self.enemySide) == 5:
            for i in self.remainList:
                ownSideTemp = list(self.ownSide)
                ownSideTemp.append(i)
                
                radiantWinRate = self.model.predictProba(ownSideTemp,
                                                         self.enemySide)[1]
                direWinRate = self.model.predictProba(self.enemySide,
                                                      ownSideTemp)[0]                
                winRate = (radiantWinRate + direWinRate) / 2.0
                self.heroWinRate[i] = winRate
            
            self.avgWinRate = sum(self.heroWinRate.values()) / len(self.heroWinRate)
            return 
    
        """
        MCTS迭代
        """
        remainHeroNum = 10 - len(self.enemySide) - len(self.ownSide)
        remainOwnSideNum = len(self.ownSide)
        remainEnemySideNum = len(self.enemySide)
        root = Node(heroId=None,nextLayer=None)
        #初始化firstLayer，从己方开始轮流选
        firstLayer = TreeLayer(remainList=self.remainList,
                               side=True,
                               parentNode=root)
        root.setNextLayer(firstLayer)
        
        while True:
            layer = firstLayer
            #ownSideNodeStack = []
            #enemySideNodeStack = []
            ownSideHeroStack = []
            enemySideHeroStack = []
            heroStack = []
            layerStack = []
            nodeStack = []
            side = True
            for i in range(0,remainHeroNum):
                """
                当双方英雄都还没选完时
                i=偶数，side=True(ownSide)
                i=奇数，side=False(enemySide)
                当有一方英雄已经选满，另一方还没选满时
                side==没选完的一方
                """
                node = self.selectNode(layer)
                nodeStack.append(node)
                heroStack.append(node.getHeroId())
                layerStack.append(layer)
                #已经到叶节点
                if i == (remainHeroNum - 1):
                    continue
                
                #node后无layer则初始化layer，传入当前的remainList
                #node后有layer则将当前layer指向node.nextLayer
                if node.nextLayer != None:
                    layer = node.nextLayer
                else:
                    remainList = list(set(self.remainList)
                                        .difference(set(heroStack)))
                    layer = TreeLayer(remainList=remainList,
                                      side=side,
                                      parentNode=node)
            
            #用选择的heroStack进行胜率预测
            ownSideTemp = list(self.ownSide)
            ownSideTemp.extend(ownSideHeroStack)
            enemySideTemp = list(self.enemySide)
            enemySideTemp.extend(enemySideHeroStack)
            #ownside winrate
            radiantWinRate = self.model.predictProba(ownSideTemp,
                                                     self.enemySide)[1]
            direWinRate = self.model.predictProba(self.enemySide,
                                                  ownSideTemp)[0]                
            ownSideWinRate = (radiantWinRate + direWinRate) / 2.0
            #enemyside winrate
            radiantWinRate = self.model.predictProba(ownSideTemp,
                                                     self.enemySide)[0]
            direWinRate = self.model.predictProba(self.enemySide,
                                                  ownSideTemp)[1]                
            enemySideWinRate = (radiantWinRate + direWinRate) / 2.0
            
            #backpropagation更新nodeStack和layerStack中的参数
            result = (ownSideWinRate,enemySideWinRate)
            self.backPropagation(nodeStack=nodeStack,
                                 layerStack=layerStack,
                                 result=result)
    
    def backPropagation(self,nodeStack,layerStack,result):
        """
        更新nodeStack和layerStack的参数
        """
        stack = zip(nodeStack,layerStack)
        for node,layer in stack:
            node.playedTimes += 1
            layerStack.playedTimes += 1
            if layer.side == True:            
                node.totalWinRate += result[0]
            else:
                node.totalWinRate += result[1]
                    
    
    def selectNode(self,layer):
        """
        根据ucb算法选择节点
        如果该层有从未选择过得Hero则优先选择，否则选ucb值最大的
        """
        if len(layer.heroToBeSelected) > 0:
            #还有没选择过的英雄，则随机选择一个
            heroId = random.sample(layer.heroToBeSelected,1)[0]
            node = Node(heroId=heroId,
                        nextLayer=None)
            return node
        
        #如果该层所有英雄都已选过，则选择ucb值最大的英雄
        node = layer.getNodeByInd(0)
        playedTimes = layer.playedTimes
        score = node.ucbScore(playedTimes)
        for i in range(1,layer.length()):
            if layer.getNodeByInd(i).ucbScore(playedTimes) > score:
                node = layer.getNodeByInd(i)
                score = node.ucbScore(playedTimes)
        
        return node
        
    def isLegalInput(self,ownSide,enemySide,heroDict):
        """
        检验输入数据是否合法
        """
        if len(ownSide) >= 5 or len(enemySide) > 5:
            print "己方英雄数量需小于5，对方英雄数量需小于等于5"
            return False
        
        if len(set(ownSide) & set(enemySide)) != 0:
            print "英雄不能复选"
            return False
        
        if not set((set(ownSide) | set(enemySide))).issubset(set(heroDict)):
            print "英雄id不符合要求"
            return False
            
        return True