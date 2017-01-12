# -*- coding: utf-8 -*-
"""
Created on Sun Jan 01 17:54:48 2017

@author: Administrator
"""
import random
from time import time
from TreeLayer import TreeLayer,Node
from BaseModel import BaseModel
from Utils import loadHeroDict

class MCTS:
    """
    基于MonteCarlo Tree Search的搜索算法
    """
    

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
        self.firstLayer = None
        self.rounds = 0
        self.avgWinRate = 0
        self.heroWinRate = {}
    
    def run(self,runTime=5):
        
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
        remainOwnSideNum = 5 - len(self.ownSide)
        remainEnemySideNum = 5 - len(self.enemySide)
        root = Node(heroId=None,nextLayer=None)
        #初始化firstLayer，从己方开始轮流选
        self.firstLayer = TreeLayer(remainList=self.remainList,
                               side=True)
        root.setNextLayer(self.firstLayer)
        
        startTime = time()
        while (time() - startTime) < runTime:
        #while True:
            layer = self.firstLayer
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
                if side == True:
                    ownSideHeroStack.append(node.getHeroId())
                else:
                    enemySideHeroStack.append(node.getHeroId())
                #已经到叶节点
                if i == (remainHeroNum - 1):
                    continue
                
                #模拟双方轮流选人
                if ((len(ownSideHeroStack) < remainOwnSideNum) 
                    and (len(enemySideHeroStack) < remainEnemySideNum)):
                            
                    side = not side
                elif (len(ownSideHeroStack) < remainOwnSideNum):
                    side = True
                else:
                    side = False
                    
                #node后无layer则初始化layer，传入当前的remainList
                #node后有layer则将当前layer指向node.nextLayer
                if node.nextLayer != None:
                    layer = node.nextLayer
                else:
                    remainList = list(set(self.remainList)
                                        .difference(set(heroStack)))
                    layer = TreeLayer(remainList=remainList,
                                      side=side)
                    node.nextLayer = layer
                

                    
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
            enemySideWinRate = 1 - ownSideWinRate
            
            #backpropagation更新nodeStack和layerStack中的参数
            result = (ownSideWinRate,enemySideWinRate)
            self.backPropagation(nodeStack=nodeStack,
                                 layerStack=layerStack,
                                 result=result)
            self.rounds += 1
        #返回计算数据
        for node in self.firstLayer.nodeSet:
            self.heroWinRate[node.getHeroId()] = node.winRate()
        
        
        
    def backPropagation(self,nodeStack,layerStack,result):
        """
        更新nodeStack和layerStack的参数
        """
        stack = zip(nodeStack,layerStack)
        for node,layer in stack:
            node.playedTimes += 1
            layer.playedTimes += 1
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
            layer.add(node)
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
    
    def getAvgWinRate(self):
        if len(self.ownSide) == 4 and len(self.enemySide) == 5:
            return self.avgWinRate
        
        return self.firstLayer.avgWinRate()
    
    def policy(self):
        """
        输出英雄选择策略，按优先级从大到小排序
        """
        if len(self.ownSide) == 4 and len(self.enemySide) == 5:
            heroWinRate = self.heroWinRate
            sortedList = sorted(heroWinRate.iteritems(), 
                                key=lambda d:d[1], reverse = True)
            herolist = []
            for i in sortedList:
                herolist.append(i[0])
            return herolist
        
        sortedList = self.firstLayer.sortByPlayedTimes()
        heroList = []
        for i in sortedList:
            heroList.append(i[0])
        
        return heroList
    

if __name__ == "__main__":
    """
    单元测试
    """    
    modelPath = "../resource/model.pkl"    
    heroDict = loadHeroDict("../resource/heroes.json")
    model = BaseModel(modelPath,heroDict)
    ownSide = [5,6,7,8]
    enemySide = [1,2,3,4]
    
    mc = MCTS(ownSide,enemySide,model,heroDict)
    mc.run(runTime=5)