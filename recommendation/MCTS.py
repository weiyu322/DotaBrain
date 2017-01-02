# -*- coding: utf-8 -*-
"""
Created on Sun Jan 01 17:54:48 2017

@author: Administrator
"""


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
        pass
    
    def run(self):
        pass
    
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