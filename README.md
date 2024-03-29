# Nomadiq Travel Recommendations
UC Berkeley MIDS, W210 Capstone (Spring 2019)

Authors: Linh Tran, Gene Ahn, James Beck

## Description

Nomadiq is a personalized travel inspiration web application to help people find their next destination. Like how Netflix recommends show or movies you may like, or how Spotify creates a discovery playlist, Nomadiq is the travel discovery platform.

## Production URl

www.thenomadiq.com

## Tech Stack & Frameworks
- Client: HTML, Javascript (JQuery)
- Server: Python (Flask), Jinja
- Cloud: AWS Sagemaker, AWS Elastic Beanstalk
- Third Party APIs / Data: Wikitravel, Instagram, Instagram-Scraper API, Bing

## Repo Contents

Repo includes the following ipython notebooks:
- nomadiq_eda: Exploratory data analysis of Instagram travel data.
- CNN_Train: Gluon code to train a location classifier using Instagram data as the training set.
- CNN_Prod: Gluon code that executes forward pass on the training model. Input are custom keywords from the user and output is the travel recommendation (e.g., 'surfing beach' --> 'San Diego'.
- TFIDF: Location recommender using content-based filtering.
- Collaborative_Filtering: Location recommender using collaborative filtering.
- wikitravel_scrape: Script to scrape Wikitravel data.

The products above were used to build the nomadiq_app, which ties both the content and collaborative filtering models with a Flask front-end. See nomadiq_app for instructions on how to set the environment and test.

## Additional Resources
- Final Presentation: https://docs.google.com/presentation/d/1gtFhi5uNplOGJ4ZnGkg4HDiBjWxBJAk2FMLubqC0nFY/edit#slide=id.g4d1954b095_0_6