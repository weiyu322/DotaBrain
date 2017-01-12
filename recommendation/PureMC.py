# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 17:07:36 2016

@author: Administrator
"""

import random
import copy
from BaseModel import BaseModel
from Utils import loadHeroDict


class PureMC:
    """
    基于纯MonteCarlo方法的英雄推荐搜索算法：
    1.在给定的当前局面下，也就是ownSide和enemySide各选择了一部分英雄
      给出当前ownSide的一个最佳英雄选择
    2.在给定的决策时间内对我方（ownSide）的所有可选英雄分别进行等量的模拟
      计算每个可选英雄的预测胜率，保存为字典

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

    
    def run(self,epochs=100):
        """
        MonteCarlo模拟主函数
        对每一个可选英雄，随机生成N个阵容局面，利用训练好的模型预测胜负概率
        因为天辉总体胜率要大于夜魇胜率，训练出的模型倾向预测天辉
        所以在计算胜率时，取己方分配到天辉和夜魇两方时的胜率的平均值
        """

        
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
        对每个己方可选英雄，再从可选集随机选择一组英雄，填补双方空缺位置形成5V5的局面
        """
        #双方待选人数
        ownSideGap = 5 - len(self.ownSide)          
        enenmySideGap = 5 - len(self.enemySide)
        
        
        for hero in self.remainList:
            #将hero从当前可选集中剔除
            remainListTemp = copy.deepcopy(self.remainList)
            remainListTemp.remove(hero)
            #将hero加入ownSide
            ownSideTemp = copy.deepcopy(self.ownSide)
            ownSideTemp.append(hero)
            enemySideTemp = copy.deepcopy(self.enemySide)
            totalWinRate = 0
            
            for i in range(epochs):
                #从可选集中随机选择英雄加入双方阵容
                chosenHeros = random.sample(remainListTemp,
                                            ownSideGap + enenmySideGap -1)
                ownSideTemp.extend(chosenHeros[0:(ownSideGap - 1)])
                enemySideTemp.extend(chosenHeros[(ownSideGap - 1):])
                
                #根据随机生成的阵容预测胜率
                radiantWinRate = self.model.predictProba(ownSideTemp,
                                                         enemySideTemp)[1]
                direWinRate = self.model.predictProba(enemySideTemp,
                                                      ownSideTemp)[0]                
                winRate = (radiantWinRate + direWinRate) / 2.0
                totalWinRate += winRate
            
            self.heroWinRate[hero] = totalWinRate / epochs
        
        self.avgWinRate = sum(self.heroWinRate.values()) / len(self.heroWinRate)
        
        return
        
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
        
    def getHeroWinRate(self):
        return self.heroWinRate
    
    def getAvgWinRate(self):
        return self.avgWinRate
    
    def policy(self):
        heroWinRate = self.heroWinRate
        sortedList = sorted(heroWinRate.iteritems(), 
                                key=lambda d:d[1], reverse = True)
        heroList = []
        for i in sortedList:
            heroList.append(i[0])
            
        return heroList
    
    def getAvgWinRate(self):
        return self.avgWinRate
if __name__ == "__main__":
    """
    单元测试
    """    
    modelPath = "../resource/model.pkl"    
    heroDict = loadHeroDict("../resource/heroes.json")
    model = BaseModel(modelPath,heroDict)
    ownSide = [5,6,7]
    enemySide = [1,2,3]
    
    mc = PureMC(ownSide,enemySide,model,heroDict)
    mc.run()