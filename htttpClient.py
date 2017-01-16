# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 23:08:39 2016

@author: Administrator
"""

import requests
import json

ownSide = ["Anti-Mage","Axe","Bane","Bloodseeker"]
enemySide = ["Crystal Maiden","Drow Ranger","Earthshaker","Juggernaut"]
radiant = [1,2,3,4,5]
dire = [6,7,8,9,10]
headers = {'Content-type': 'application/json'}
match1 = {'ownSide': ownSide,
         'enemySide': enemySide,
         'topK':3}
match2 = {"radiant":radiant,
          "dire":dire}
          
recommend = requests.post("http://localhost:5000/api/v1.0/recommend",
                          headers=headers,
                          data=json.dumps(match1))
"""
predict = requests.post("http://localhost:5000/api/v1.0/predict",
                        headers=headers,
                        data=json.dumps(match2))
"""
print recommend.text
#print predict.text