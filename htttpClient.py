# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 23:08:39 2016

@author: Administrator
"""

import requests
import json

headers = {'Content-type': 'application/json'}
match = {'ownSide': ownSide,
         'enemySide': enemySide,
         'topK':3}

r = requests.post("http://localhost:5000/api/v1.0/recommend",
                  headers=headers,
                  data=json.dumps(match))
print r.text