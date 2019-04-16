from flask import Flask
# from flask_login import LoginManager
# import boto
# import boto.s3.connection

# add application variable for Elastic Beanstalk
application = app = Flask(__name__)


# def download_data_connect_to_region(region, access_key, secret_key, bucket_name, key, local_path):
#     '''This will use connect_to_region() function in boto'''
#     conn = boto.s3.connect_to_region(
#             region_name=region,
#             aws_access_key_id=access_key,
#             aws_secret_access_key=secret_key,
#             calling_format=boto.s3.connection.OrdinaryCallingFormat()
#             )
#     bucket = conn.get_bucket(bucket_name)
#     key = bucket.get_key(key)
#     key.get_contents_to_filename(local_path)
#     print('Downloaded File {} to {}'.format(key, local_path))
#
# region = 'us-east-1'
# access_key = 'AKIAIQJ73BYFFESKMHXA'
# secret_key = 'XAzVgRJNonnCH0M0lc7S6dkwRwG/SLScjgQnsSp'
# bucket_name = 'sagemaker-nomadiq-data'
# keys = ['tfidf_artifacts.pickle', 'collab_filter_artifacts.pickle']
# local_paths = ['/nomadiq_app/static/data/tfidf_artifacts.pickle','/nomadiq_app/static/data/collab_filter_artifacts.pickle']
#
# for key,local_path in zip(keys,local_paths):
#     download_data_connect_to_region(region, access_key, secret_key, bucket_name, key, local_path)

from nomadiq_app import routes


# this allows for us to run this with python
# if __name__ == '__main__':
#     app.run(debug=True)
