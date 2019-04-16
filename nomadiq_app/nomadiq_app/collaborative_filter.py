# General libraries.
import numpy as np
import pandas as pd
import pickle
import boto3
import sys

# # Set S3 environment
# client = boto3.client('s3')
# resource = boto3.resource('s3')
# my_bucket = resource.Bucket('sagemaker-nomadiq-data')
# # for object in my_bucket.objects.all():
# #     print(object)
# my_bucket.download_file('collab_filter_artifacts.pickle','collab_filter_artifacts.pickle')

# # Load/Open pickle files
# with open('collab_filter_artifacts.pickle', 'rb') as f:
#     df_travel_features,cosine_sim,city_dict,popular_cities = pickle.load(f)

def collab_get_recommendations_city(places_visited,df_travel_features,cosine_sim,city_dict,popular_cities, X_tfidf,vectorizer,indices2):
    '''Enter a list of cities and get recommendations back
    You can enter multiple cities delimited by comma (no space)'''
    places_visited = places_visited.split(",")
    places_visited = [place.title() for place in places_visited]
    # print(places_visited)
    user_vector = []
    for location in df_travel_features.index:
        if location in places_visited:
            user_vector.append(1)
        else:
            user_vector.append(0)

    # Append travel predictions to a list
    user_rating = []
    # Loop through each location in the cosine sim matrix
    for index in range(len(cosine_sim)):
        numerator = []
        denominator = []
        # If the user has not visited the location
        if user_vector[index] == 0:
            # Loop through pairwise similarities of the given locations
            for index2 in range(len(cosine_sim[index])):
                # Pairwise similarity times whether the user has visited the location
                numerator.append(cosine_sim[index][index2] * user_vector[index2])
                denominator.append(cosine_sim[index][index2])
            user_rating.append(sum(numerator)/sum(denominator))

        else:
            user_rating.append(0)
    # Get indices of top 10 ranked cities
    indices = sorted(range(len(user_rating)), key=lambda i: user_rating[i], reverse=True)[:10]
    # print(indices)
    ratings_list = sorted(user_rating,reverse=True)
    recommendations = []
    for index in range(len(indices)):
        if ratings_list[index] > 0:
            recommendations.append(df_travel_features.index[indices[index]])
        else:
            # print(popular_cities[:10-index])
            recommendations = recommendations + popular_cities[:10-index]
            break
    city_recs = []
    loop_count = 0

    # Get TFIDF words
    dense_matrix = X_tfidf.toarray()
    vocab_dict = vectorizer.vocabulary_
    vocab_reverse = {y:x for x,y in vocab_dict.items()}

    for city in recommendations:
        # Get top (3) words associated with city
        city_index = list(indices2).index(city.title())
        top_word_index = sorted(range(len(dense_matrix[city_index])), key=lambda i: dense_matrix[city_index][i], reverse=True)[:3]
        # create JSON recommendation
        city_recs.append({"location_id": city_dict[city], "location_name": city, "cosine_similarity": ratings_list[loop_count],"top_words": [vocab_reverse[word] for word in top_word_index]})
        loop_count += 1
    return city_recs

# get_recommendations_city(sys.argv[1])
