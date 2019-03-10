# General libraries.
import re
import numpy as np
import pandas as pd
import json
import pickle
import boto3
import sys
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import *

# Set S3 environment
client = boto3.client('s3')
resource = boto3.resource('s3')
my_bucket = resource.Bucket('sagemaker-nomadiq-data')

# Load/Open pickle files
with open(r'tfidf_artifacts.pickle', 'rb') as f:
    cosine_sim,indices,reverse_indices,vectorizer,X_tfidf,city_dict = pickle.load(f)

# Clean string with preprocessing regex rules
def clean_str(string):
    """
    Tokenization/string cleaning for all datasets
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    string = re.sub(r"<b>", " ", string)
    string = re.sub(r"</b>", " ", string)
    string = re.sub(r"<br>", " ", string)
    string = re.sub(r"</br>", " ", string)
    string = re.sub(r"<p>", " ", string)
    string = re.sub(r"</p>", " ", string)
    string = re.sub(r"<ul>", " ", string)
    string = re.sub(r"</ul>", " ", string)
    string = re.sub(r"<li>", " ", string)
    string = re.sub(r"</li>", " ", string)
    return string.strip().lower()

def get_recommendations_city(city, cosine_sim=cosine_sim):
    city = city.title()
    idx = reverse_indices[city]
    # Get the pairwise similarity scores of all cities
    sim_scores = list(enumerate(cosine_sim[idx]))
    # Sort the cities based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Get the scores of the 10 most similar cities
    sim_scores = sim_scores[1:11]
    # Get the city indices
    city_indices = [i[0] for i in sim_scores]
    city_recs = []
    loop_count = 0
    for city in indices.iloc[city_indices]:
        city_recs.append({"location_id": city_dict[city], "location_name": city, "cosine_similarity": sim_scores[loop_count][1]})
        loop_count += 1
    # Return the top 10 most similar cities
    print(json.dumps(city_recs))
    return json.dumps(city_recs)

# city_input = input(sys.argv)
get_recommendations_city(sys.argv[1])
