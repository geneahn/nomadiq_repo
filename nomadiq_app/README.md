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

## Test Application Locally

To test the site locally on your computer, follow these instructions:

System Requirements:
- Note: the zipped version of nomadiq_app contains necessary pickle artifacts.
- Make sure required packages are installed (see setup.py or requirements.txt). Install required packages with step 4 below.
- Clone the web files to a local repository


Test on Flask Application on your local or virtual machine
Note: instructions below are for debug mode.

1. From your terminal, navigate to the parent directory nomadiq_app (where run.py) is stored
2. Set environment variable for the flask application: ```export FLASK_APP=run.py```
3. (For testing only) Set the environment to debug mode with two options: ```export FLASK_DEBUG=1``` or ```set FLASK_ENV=development```
4. To check for package requirements, install the app packages with ```pip install -e .```
5. Start the server: ``flask run``` or ```python run.py```
6. Copy and paste the URL in the terminal to your browser to view/test the application; url should be: http://127.0.0.1:5000/

## Acknowledgements
1. W3 Schools for CSS Templates.
2. Core Schafer for Flask Blog tutorial and code samples used for prototyping login/signup: https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog
3. Instagram-Scraper by Richard Arcega: https://github.com/rarcega
