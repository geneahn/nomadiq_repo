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
# for object in my_bucket.objects.all():
#     print(object)

# Get all tfidf artifacts from S3
# These artifacts were built in a separate TFIDF.ipynb notebook
my_bucket.download_file('tfidf_artifacts.pickle','tfidf_artifacts.pickle')

# Load/Open pickle files
with open('tfidf_artifacts.pickle', 'rb') as f:
    cosine_sim,indices,reverse_indices,vectorizer,X_tfidf,city_dict = pickle.load(f)

# Clean string with preprocessing regex rules
# Modified from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
def clean_str(string):
    """
    Tokenization/string cleaning for all datasets
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

def get_recommendations_keywords(doc, cosine_sim=cosine_sim):
    '''Input set of list of keywords and cosine similarity matrix
    and return top 10 city recommendations'''
    test_tfidf = vectorizer.transform([clean_str(doc)])
    cosine_sim_test = linear_kernel(test_tfidf, X_tfidf)
    sim_scores = list(enumerate(cosine_sim_test[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[0:10]
    city_indices = [i[0] for i in sim_scores]
    city_recs = []
    loop_count = 0
    for city in indices.iloc[city_indices]:
        city_recs.append({"location_id": city_dict[city], "location_name": city, "cosine_similarity": sim_scores[loop_count][1]})
        loop_count += 1
    # Return the top 10 most similar cities
    print(json.dumps(city_recs))
    return json.dumps(city_recs)

get_recommendations_keywords(sys.argv[1])
