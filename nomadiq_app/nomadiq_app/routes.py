#import python foundation packages
from flask import render_template, url_for, request, jsonify
import json
import pickle
import re
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import *

# import app packages
from nomadiq_app import app
import nomadiq_app.signup_login as auth
import nomadiq_app.wikitravel_scrape as wikitravel
import nomadiq_app.poi_scrape as ps
import nomadiq_app.collaborative_filter as cf
import nomadiq_app.city_recommendation as cr
import nomadiq_app.keyword_recommendation as kr


# global variables default
recommendation_header = "Popular Travel Locations"
search_filter_header = ""
search_value = ""
TRAVELWORDS = ["beautiful","food","attraction"]

# load TFIDF to server for city / keyword recommendations
with open(r'nomadiq_app/static/data/tfidf_artifacts.pickle', 'rb') as f:
    cosine_sim,indices,reverse_indices,vectorizer,X_tfidf,city_dict = pickle.load(f)

# Load/Open pickle files
with open('nomadiq_app/static/data/collab_filter_artifacts.pickle', 'rb') as f:
    df_travel_features,cosine_sim_c,city_dict_c,popular_cities_c = pickle.load(f)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/home/about")
def about():
    return render_template("home.html",section="about")

@app.route("/welcome")
def welcome():
    return render_template("welcome.html",text_guide="enter cities, separated by comma")

@app.route("/discover")
def discover():
    return render_template('discover.html', text_guide="My favorite location (single)")


@app.route("/collaborative_recommend",methods=["POST"])
def collaborative_recommend():
    # get search values
    seed_cities = request.form.get("seed_cities")
    # try:
    new_rec_list = cf.collab_get_recommendations_city(seed_cities,df_travel_features,cosine_sim_c,city_dict_c,popular_cities_c, X_tfidf,vectorizer,indices)
    print(vectorizer)
    # scrape image
    for item in new_rec_list:
        img_url, page = wikitravel.get_img(item["location_name"])
        item.update( {'wikitravel_page' : page} )
        item.update( {'image_url' : img_url} )
        # item.update( {'poi_list' : ps.get_poi_img2(item["location_name"],item["top_words"])})
        item.update( {'poi_list' : ps.get_poi_img2(item["location_name"],TRAVELWORDS)})
    return render_template('results.html', recommendation_header="Recommended places for you.", search_filter_header="These recommendations are based on your travel history: ",search_value=seed_cities, rec_list=new_rec_list)
    # except:
    #     return render_template("welcome.html",text_guide="Unable to find results for "+str(seed_cities))

@app.route("/recommend_city",methods=["POST"])
def recommend_city():
    # get search values
    seed_city = request.form.get("seed_city")
    # try:
    new_rec_list = cr.get_recommendations_city(seed_city,cosine_sim,indices,reverse_indices,vectorizer,X_tfidf,city_dict)
    # scrape image
    for item in new_rec_list:
        img_url, page = wikitravel.get_img(item["location_name"])
        item.update( {'wikitravel_page' : page} )
        item.update( {'image_url' : img_url} )
        # item.update( {'poi_list' : ps.get_poi_img2(item["location_name"],item["top_words"])})
        item.update( {'poi_list' : ps.get_poi_img2(item["location_name"],TRAVELWORDS)})
    return render_template('results.html', recommendation_header="Recommended places for you.", search_filter_header="Showing cities similar to ",search_value=seed_city, rec_list=new_rec_list)
    # except:
    #     return render_template("discover.html",text_guide="Unable to find results for "+str(seed_city))

@app.route("/recommend_keyword",methods=["POST"])
def recommend_keyword():
    # get search values
    keyword = request.form.get("keyword")
    # try:
    keyword_rec_list = kr.get_recommendations_keywords(keyword,cosine_sim,indices,vectorizer,X_tfidf,city_dict)
    print(keyword_rec_list)
    # scrape image
    for item in keyword_rec_list:
        img_url, page = wikitravel.get_img(item["location_name"])
        item.update( {'wikitravel_page' : page} )
        item.update( {'image_url' : img_url} )
        # item.update( {'poi_list' : ps.get_poi_img2(item["location_name"],item["top_words"])})
        item.update( {'poi_list' : ps.get_poi_imgk(item["location_name"],keyword)})
    return render_template('results.html', recommendation_header="Recommended places for you.", search_filter_header="Recommendation based on keyword:",search_value=keyword, rec_list=keyword_rec_list)
    # except:
    #     return render_template("discover.html",text_guide="Unable to find results for "+str(keyword))

@app.route("/login")
def login():
    return "Login function under construction."

@app.route("/recommend_POI")
def recommend_poi():
    return "POI function under construction."

@app.route("/plan")
def plan():
    return "Plan function under construction."
