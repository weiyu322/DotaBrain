# -*- coding: utf-8 -*-
"""
Created on Sun Jan 01 17:54:48 2017

@author: Administrator
"""
import copy
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
                ownSideTemp = copy.deepcopy(self.ownSide)
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
        root = Node(heroId=None,nextLayer=None)
        #初始化firstLayer，从己方开始轮流选
        firstLayer = TreeLayer(remainList=self.remainList,
                               side=True,
                               parentNode=root)
        root.setNextLayer(firstLayer)
        
        while True:
            layer = firstLayer
            nodeStack = []
            heroStack = []
            layerStack = []
            side = True
            for i in range(0,remainHeroNum):
                
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
            
            #backpropagation更新nodeStack和layerStack中的参数
            self.pr
    
    def backPropagation(self,nodeStack,layerStack,result):
        pass
    
                    
    
    def selectNode(self,layer):
        """
        """
        if layer.length == 0:
            return None
        
        node = layer.getNodeByInd(0)
        score = node.getUcbScore()
        for i in range(0,layer.length()):
            if layer.getNodeByInd(i).getUcbScore() > score:
                node = layer.getNodeByInd(i)
                score = node.getUcbScore()
        
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