# General libraries.
import re
import numpy as np
import pandas as pd
# import json
# import pickle
# import boto3
# import sys
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import *


# # Set S3 environment
# client = boto3.client('s3')
# resource = boto3.resource('s3')
# my_bucket = resource.Bucket('sagemaker-nomadiq-data')
# # for object in my_bucket.objects.all():
# #     print(object)
#
# my_bucket.download_file('tfidf_artifacts.pickle','tfidf_artifacts.pickle')
#
# Load/Open pickle files
# with open(r'nomadiq_app/static/data/tfidf_artifacts.pickle', 'rb') as f:
#     cosine_sim,indices,reverse_indices,vectorizer,X_tfidf,city_dict = pickle.load(f)

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

def get_recommendations_keywords(doc,cosine_sim,indices,vectorizer,X_tfidf,city_dict):
    test_tfidf = vectorizer.transform([clean_str(doc)])
    cosine_sim_test = linear_kernel(test_tfidf, X_tfidf)
    sim_scores = list(enumerate(cosine_sim_test[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[0:10]
    city_indices = [i[0] for i in sim_scores]
    city_recs = []
    loop_count = 0
    # Get TFIDF words
    dense_matrix = X_tfidf.toarray()
    vocab_dict = vectorizer.vocabulary_
    vocab_reverse = {y:x for x,y in vocab_dict.items()}
    for city in indices.iloc[city_indices]:
        # Get top (3) words associated with city
        city_index = list(indices).index(city.title())
        top_word_index = sorted(range(len(dense_matrix[city_index])), key=lambda i: dense_matrix[city_index][i], reverse=True)[:3]
        # Create JSON for city recs
        city_recs.append({"location_id": city_dict[city], "location_name": city, "cosine_similarity": sim_scores[loop_count][1],"top_words": [vocab_reverse[word] for word in top_word_index]})
        loop_count += 1
    # Return the top 10 most similar cities
    # print(json.dumps(city_recs))
    # return json.dumps(city_recs)
    return city_recs

# get_recommendations_keywords(sys.argv[1])
