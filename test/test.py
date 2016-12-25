# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 17:07:36 2016

@author: Administrator

测试sklearn模型预测速度
LR模型，222维特征
numpy生成10万条样本和对单条样本循环预测10万次

单条预测时间是矩阵预测时间的100倍
"""

import pickle
from time import time
import numpy as np

f = open("../resource/model.pkl","rb")

model = pickle.load(f)

feature = np.reshape(np.random.random(size=222),[1,-1])
features = np.random.rand(10000,222)

start1 = time()
for i in range(10000):
    model.predict_proba(feature)

end1 = time()
print "single time: %f s" % (end1-start1)

start2 = time()
model.predict_proba(features)
end2 = time()
print "multiple time: %f s" % (end2-start2)

