from nomadiq_app import app

from flask import Flask, render_template, url_for, request
import json
import pickle
import nomadiq_app.image_scrape as ims
import nomadiq_app.poi_scrape as ps
import nomadiq_app.collaborative_filter as cf
import nomadiq_app.city_recommendation as cr
import nomadiq_app.keyword_recommendation as kr
# from nomadiq_app.image_scrape import * #as img_scr
# from nomadiq_app.poi_scrape import * #as ps
# from nomadiq_app.city_recommendation import * #as cr
# from nomadiq_app.keyword_recommendation import * #as kr
# from nomadiq_app.collaborative_filter import * #as cf
import re
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import *

# Set up page default parameters
recommendation_header = "Popular Travel Locations"
search_filter_header = ""
search_value = ""

# load TFIDF to server for city / keyword recommendations
with open(r'nomadiq_app/static/data/tfidf_artifacts.pickle', 'rb') as f:
    cosine_sim,indices,reverse_indices,vectorizer,X_tfidf,city_dict = pickle.load(f)

# Load/Open pickle files
with open('nomadiq_app/static/data/collab_filter_artifacts.pickle', 'rb') as f:
    df_travel_features,cosine_sim_c,city_dict_c,popular_cities_c = pickle.load(f)

@app.route("/")
@app.route("/welcome")
def welcome():
    return render_template("welcome.html",text_guide="enter cities, separated by comma (no space)")

@app.route("/discover")
def discover():
    return render_template('discover.html', text_guide="My favorite location (single)")


@app.route("/collaborative_recommend",methods=["POST"])
def collaborative_recommend():
    # get search values
    seed_cities = request.form.get("seed_cities")
    poi_list = {}
    try:
        new_rec_list = cf.collab_get_recommendations_city(seed_cities,df_travel_features,cosine_sim_c,city_dict_c,popular_cities_c)
        poi_list = {}
        # scrape image
        for item in new_rec_list:
            url = ims.get_img(item["location_name"])
            item.update( {'image_url' : url} )
            poi_list.update({item["location_name"]:ps.get_poi_img(item["location_name"],3)})
            # poi_list.update({item["location_name"]:ps.get_ig_most_recent(item["location_name"],3)})
        return render_template('results.html', recommendation_header="Recommended Cities for you.", search_filter_header="Showing cities similar to ",search_value=seed_cities, rec_list=new_rec_list, poi_list=poi_list)
    except:
        return render_template("welcome.html",text_guide="Unable to find results for "+str(seed_cities))

@app.route("/recommend_city",methods=["POST"])
def recommend_city():
    # get search values
    seed_city = request.form.get("seed_city")
    poi_list = {}
    try:
        new_rec_list = cr.get_recommendations_city(seed_city,cosine_sim,indices,reverse_indices,vectorizer,X_tfidf,city_dict)
        # scrape image
        for item in new_rec_list:
            url = ims.get_img(item["location_name"])
            item.update( {'image_url' : url} )
            poi_list.update({item["location_name"]:ps.get_poi_img(item["location_name"],3)})
        return render_template('results.html', recommendation_header="Recommended Cities for you.", search_filter_header="Showing cities similar to ",search_value=seed_city, rec_list=new_rec_list, poi_list=poi_list)
    except:
        return render_template("discover.html",text_guide="Unable to find results for "+str(seed_city))

@app.route("/recommend_keyword",methods=["POST"])
def recommend_keyword():
    # get search values
    keyword = request.form.get("keyword")
    poi_list = {}
    try:
        keyword_rec_list = kr.get_recommendations_keywords(keyword,cosine_sim,indices,reverse_indices,vectorizer,X_tfidf,city_dict)
        # scrape image
        for item in keyword_rec_list:
            url = ims.get_img(item["location_name"])
            item.update( {'image_url' : url} )
            poi_list.update({item["location_name"]:ps.get_poi_img(item["location_name"],3)})
        return render_template('results.html', recommendation_header="Recommended Cities for you.", search_filter_header="Recommendation based on keyword:",search_value=keyword, rec_list=keyword_rec_list, poi_list=poi_list)
    except:
        return render_template("discover.html",text_guide="Unable to find results for "+str(keyword))

@app.route("/login")
def login():
    return "Login function under construction."

@app.route("/recommend_POI")
def recommend_poi():
    return "POI function under construction."

@app.route("/plan")
def plan():
    return "Plan function under construction."
