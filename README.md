# DotaBrain
A Dota2 Hero Recommendation Engine Based On MachineLearning Techs And MonteCarlo Search

## Introduction
- DotaBrain is a dota2 game hero recommendation engine using machine learning and artificial intelligence technology.
- DotaBrain learns a predictive model that maps the hero composition of both team to the match outcome, the predictive accuracy exceeds that of many experienced players in a test.
- Based on this predictive model, DotaBrain further uses [MonteCarlo Tree Search](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search) algorithm which is a key algorithm for many board games AI like [AlphaGo](https://en.wikipedia.org/wiki/AlphaGo) to provide players with real-time hero recommendation.

## Framework
![image](https://github.com/weiyu322/DotaBrain/blob/master/resource/framework.png)

## Requirements
1.flask<br>
2.scikit-learn<br>
3.numpy

## Getting Started
### Install
```
git clone https://github.com/weiyu322/DotaBrain.git
```
### Start Web App
```
cd DotaBrain/
python app.py
```
### Using APIs
The web server provides two APIs: prediction API and recommendation API
*prediction api: given the full hero composition of a match(10 heroes), return the predicitve result of the match 
  *request form
  ``` 
  POST /api/v1.0/predict HTTP/1.1
  Content-type: application/json
  Host: localhost:5000

  {
    "radiant": ["Anti-Mage","Axe","Bane","Bloodseeker","Crystal Maiden"],
    "dire": ["Drow Ranger","Earthshaker","Juggernaut","Mirana","Morphling"]
  }
  ```
  *response form
  ```
  HTTP/1.1 200 OK
  Date: Thu, 12 Jan 2017 08:34:15 GMT
  Content-Type: application/json
  Server: Werkzeug/0.11.4 Python/2.7.12
  
  {
    "radiantWinRate": 0.48737193751218433,
    "direWinRate": 0.51262806248781567
  }
  ```
*recommendation api: given part of hero composition of a match(< 10 heroes), return topK hero recommendations
  *request form
  ```
  POST /api/v1.0/recommend HTTP/1.1
  Content-type: application/json
  Host: localhost:5000
  
  {
    "ownSide": ["Anti-Mage","Axe","Bane"],
    "enemySide": ["Bloodseeker","Crystal Maiden","Drow Ranger"]
    "topK": 3
  }
  ```
  *response form
  ```
  HTTP/1.1 200 OK
  Date: Thu, 12 Jan 2017 08:34:15 GMT
  Content-Type: application/json
  Server: Werkzeug/0.11.4 Python/2.7.12
  
  {
    "avgWinRate": 0.33632085184454052, 
    "recommendation": [
      "Centaur Warrunner", 
      "Venomancer", 
      "Omniknight"
    ]
  }
  ```
