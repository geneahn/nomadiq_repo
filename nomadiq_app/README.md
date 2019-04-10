# Nomadiq Travel Recommendations
UC Berkeley MIDS, W210 Capstone (Spring 2019)

Authors: Linh Tran, Gene Ahn, James Beck

## Description

Nomadiq is a personalized travel discovery tool to help people find their next destination. Like how Netflix recommends shows you may like, or Spotify creates a discovery playlist, Nomadiq is the travel analog.

## Production URl

TBD

## Test Application Locally

To test the site locally on your computer, follow these instructions:

System Requirements:
- Make sure flask is installed, using ```pip install flask```
- Clone the web files to a local repository

Test on Flask Application on your local or virtual machine
Note: instructions below are for debug mode, which allows you to save updates to your server instantly.

1. From your terminal, navigate to the directory where nomadiq.py is stored
2. Set environment variable for the flask application: ```export FLASK_APP=nomadiq_app```
3. Set the environment to debug mode with two options: ```export FLASK_DEBUG=1``` or ```set FLASK_ENV=development```
4. If setting up for the first time, install the app packages with ```pip install -e .```
4. Start the server: ``flask run``` or ```python nomadiq_app.py```
5. Copy and paste the URL in the terminal to your browser to view/test the application; url should be: http://127.0.0.1:5000/

## Past Prototypes
TBD
