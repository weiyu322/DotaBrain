# -*- coding: utf-8 -*-
"""
Created on Mon Aug 01 20:27:57 2016

@author: Administrator
"""

import numpy as np
import pandas as pd
import json

f = open("../resource/heroes.json")
heroes = json.load(f)
f.close()
heroes = heroes["heroes"]
herolist = {}
for i in heroes:
    herolist[i["id"]] = i["localized_name"]
newheroid = {}
count = 0
for i in herolist:
    newheroid[i] = count
    count += 1

def preprocessing(df):
    
    df_sub = df.iloc[:,7:17]
    data = []
    radiant_hero = ["players.0.hero_id","players.1.hero_id","players.2.hero_id","players.3.hero_id","players.4.hero_id"]
    dire_hero = ["players.5.hero_id","players.6.hero_id","players.7.hero_id","players.8.hero_id","players.9.hero_id"]
    for index,row in df_sub.iterrows():
        temp = [0] * 222
        for col in df_sub.columns:
            if col in radiant_hero:
                temp[newheroid[row[col]]] = 1
            else:
                temp[newheroid[row[col]] + 111] = 1
        data.append(temp)
    radiant_col = ["radiant_%s" % i for i in range(111)]
    dire_col = ["dire_%s" % i for i in range(111)]
    col = radiant_col + dire_col
    dataset = pd.DataFrame(data,columns=col)
    
    label = df.radiant_win.map(trans).values
    #dataset["match_id"] = df.match_id.values
    return dataset,label

def trans(x):
    if x == True:
        return 1
    else:
        return 0
