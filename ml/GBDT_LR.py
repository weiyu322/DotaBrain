# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 17:03:12 2016

@author: Administrator
"""

import pandas as pd
import preprocessing
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score,roc_curve
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import matplotlib.pyplot as plt


class gbdt_lr():
    
    grd = None        #gbdt model
    lr = None         #lr model
    grd_enc = None    #onehotencoder
    
    def __init__(self,grd,lr):
        self.grd = grd
        self.lr = lr
    
    def fit(self,x,y):
        
        #train gbdt
        self.grd.fit(x,y)
        
        #encode new feature
        self.grd_enc = OneHotEncoder(sparse=False)
        self.grd_enc.fit(self.grd.apply(x)[:,:,0])
        gbdt_feature = self.grd_enc.transform(self.grd.apply(x)[:,:,0])
        
        #concat original feature and new feature
        x_train = np.column_stack((x,gbdt_feature))
        
        #train lr
        self.lr.fit(x_train,y)
        
    
    def predict(self,x):
        
        x_new = self.transform(x)
        return self.lr.predict(x_new)
    
    def predict_proba(self,x):
        
        x_new = self.transform(x)
        return self.lr.predict_proba(x_new)
    
    def transform(self,x):
        """
        x: original data
        x_new : dataset with new features extraced by gbdt model
        """
        enc = self.grd_enc.transform(self.grd.apply(x)[:,:,0])
        x_new = np.column_stack((x,enc))
        
        return x_new
    
if __name__ == "__main__":
    #Read Data
    print 'Read data...'
    df1 = pd.read_csv('E:/dota2/datasets/train.csv')
    df2 = pd.read_csv('E:/dota2/datasets/test1.csv')
    df3 = pd.read_csv('E:/dota2/datasets/test2.csv')

    #Preprocessing
    print 'Preprocessing...'
    x_train,y_train = preprocessing.preprocessing(df1)
    x_test,y_test = preprocessing.preprocessing(df2)
    x_test2,y_test2 = preprocessing.preprocessing(df3)
    
    #gbdt and lr model
    grd = GradientBoostingClassifier(n_estimators=100,max_depth=5)
    lr = LogisticRegression()
    
    
    #gbdt+lr
    clf = gbdt_lr(grd,lr)
    clf.fit(x_train,y_train)
    print "train accuracy: %f" % accuracy_score(y_train,clf.predict(x_train))
    print "test accuracy: %f" % accuracy_score(y_test,clf.predict(x_test))
    #print "auc: %f" % roc_auc_score(y_test,clf.predict_prob(x_test)[:,1])
    
    #lr alone
    lr_alone = LogisticRegression()
    lr_alone.fit(x_train,y_train)
    print "train accuracy: %f" % accuracy_score(y_train,lr_alone.predict(x_train))
    print "test accuracy: %f" % accuracy_score(y_test,lr_alone.predict(x_test))
    
    #plot roc curve
    fpr_gbdt_lr,tpr_gbdt_lr,_ = roc_curve(y_test,clf.predict_proba(x_test)[:,1])
    fpr_lr,tpr_lr,_ = roc_curve(y_test,lr_alone.predict_proba(x_test)[:,1])
    plt.figure(1)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.plot(fpr_gbdt_lr,tpr_gbdt_lr,label='GBDT+LR')
    plt.plot(fpr_lr,tpr_lr,label='LR')
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')
    plt.title('ROC curve')
    plt.legend(loc='best')
    plt.show()