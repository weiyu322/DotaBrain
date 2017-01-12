# DotaBrain
A Dota2 Hero Recommendation Engine Based On MachineLearning Techs And MonteCarlo Search

## Introduction
- DotaBrain is a dota2 game hero recommendation engine using machine learning and artificial intelligence technology.
- DotaBrain learns a predictive model that maps the hero composition of both team to the match outcome, the predictive accuracy exceeds that of many experienced players in a test.
- Based on this predictive model, DotaBrain further uses [MonteCarlo Tree Search](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search) algorithm which is a key algorithm for many board games AI like [AlphaGo](https://en.wikipedia.org/wiki/AlphaGo) to provide players with real-time hero recommendation.

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
- prediction api: given the full hero composition of a match(10 heroes), return the predicitve result of the match 
  - request form
``` 
POST
```
