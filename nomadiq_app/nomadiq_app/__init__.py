from flask import Flask
import boto

app = Flask(__name__)


# Set S3 environment
bucket_name = 'sagemaker-nomadiq-data'
keys = ['tfidf_artifacts.pickle', 'collab_filter_artifacts.pickle']
local_paths = ['/nomadiq_app/static/data/tfidf_artifacts.pickle','/nomadiq_app/static/data/collab_filter_artifacts.pickle']

client = boto3.client('s3')
resource = boto3.resource('s3')
my_bucket = resource.Bucket(bucket_name)

for key,local_path in zip(keys,local_paths):
    my_bucket.download_file(key,local_path)

import nomadiq_app.routes

# this allows for us to run this with python
if __name__ == '__main__':
    app.run(debug=True)
