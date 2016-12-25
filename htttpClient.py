# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 23:08:39 2016

@author: Administrator
"""
import httplib, urllib

ownSide = [5,6,7,8]
enemySide = [1,2,3,9,10]
params = urllib.urlencode({'ownSide': ownSide,
                           'enemySide': enemySide,
                           'topK':3})
headers = {"Content-type": "application/x-www-form-urlencoded"
                , "Accept": "text/plain"}
 
httpClient = httplib.HTTPConnection("localhost", 5000)
httpClient.request("POST", "/api/v1.0/recommend", params, headers)
 
response = httpClient.getresponse()
print response.status
print response.reason
a = response.read()