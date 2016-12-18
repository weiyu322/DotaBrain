# -*- coding: utf-8 -*-
"""
Created on Mon Aug 08 21:52:49 2016

@author: Administrator
"""

import pandas as pd
import preprocessing
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.cross_validation import train_test_split
import matplotlib.pyplot as plt

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

#model
def SVM():
    clf = LinearSVC(C=10)
    return clf

def RF():
    clf = RandomForestClassifier(n_estimators=10,max_depth=3)
    return clf

def GBDT():
    clf = GradientBoostingClassifier(n_estimators=100)
    return clf

def LR():
    clf = LogisticRegression()
    return clf

clf = LR()
"""
#train
print 'Trainning...'
clf.fit(x_train,y_train)

#Test
print "Train accuracy: %f" % accuracy_score(y_train,clf.predict(x_train))
print "Test accuracy: %f" % accuracy_score(y_test,clf.predict(x_test))
print "Test2 accuracy: %f" % accuracy_score(y_test2,clf.predict(x_test2))
print "auc: %f" % roc_auc_score(y_test,clf.predict_proba(x_test)[:,1])
"""

def learning_curve(x_train,y_train,x_test,y_test,clf,size):
    train_scores = []
    test_scores = []
    for i in size:
        X_train,_,Y_train,_ = train_test_split(x_train,y_train,test_size=1-i)
        clf.fit(X_train,Y_train)
        train_acc = accuracy_score(Y_train,clf.predict(X_train))
        test_acc = accuracy_score(y_test,clf.predict(x_test))
        train_scores.append(train_acc)
        test_scores.append(test_acc)
    return train_scores,test_scores

def plot_curve(title,train_sizes,train_scores,test_scores):
    
    plt.figure()
    plt.ylim([0.64,0.68])
    plt.title(title)
    plt.xlabel("Training Examples")
    plt.ylabel("Accuracy")
    plt.plot(train_sizes,train_scores,"o-",color="r",label="Training accuracy")
    plt.plot(train_sizes,test_scores,"o-",color="g",label="Test accuracy")
    plt.legend(loc="best")
    plt.show()

size=[0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.5,0.6,0.7,0.8,0.9,1]
train_scores,test_scores = learning_curve(x_train,y_train,x_test,y_test,clf,size)
title = "Logistic Rregression learning curve"
train_sizes = map(lambda x:x*len(x_train),size)
plot_curve(title,train_sizes,train_scores,test_scores)
