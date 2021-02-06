# Deploying-Analytics-ML-Apps
This repository contains projects and assets on deploying analytics and Machine Learning use-cases developed in python. We use Python based packages to create the use-cases and deploy through falsk and dash library The repo has three projects: 1. World GDP Analysis 2. Stock Market Analysis 3. Tweet Analysis. 

## 1. World GDP Analysis
This project provides a simple way of analysisng data using pandas and creating visualizations using dash. The data source for the use-case is gapminder which is provided as dash in-built dataset. The app is hosted on heroku <a href='https://galaxyanalytica.herokuapp.com/apps/world_gdp_analysis'>World GDP Analysis</a>
![alt text](http://url/to/img.png)

## 2. Stock Market Analysis
This use-case analyses stock-markets and deploys a forecasting model to predict market stocks. We start by scraping stocks data from the website using pandas. We process, analys and visualize the data. We create a forecasting model using fbprophet library. The model is deployed on heroku with an option of real-time model training. The app is hosted on heroku <a href='https://galaxyanalytica.herokuapp.com/apps/stock_forecasting'>Stock Forecasting</a>
![alt text](http://url/to/img.png)

## 3. Tweet Analysis

This project involves extracting tweets from the twitter website, cleaning and transforming the tweets. We analyse and visualize various aspects of the tweets. We model the sentiments of the tweets using textblob and visualize the sentiments. We create geo-spacial representations of the tweets using mapbox and geopandas. The app is hosted on heroku <a href='https://galaxyanalytica.herokuapp.com/apps/tweet_analysis'>Tweets Analysis</a>
![alt text](http://url/to/img.png)
