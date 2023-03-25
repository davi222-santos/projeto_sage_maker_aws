import os

import boto3
from dotenv import load_dotenv

load_dotenv()

bucket_name='bucketgrupo2'
key='modelo.h5'
save_path='src/resources/model.h5'

def download_model_from_s3(bucket_name, model_file_path, save_path):
    s3 = boto3.client('s3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("PRIVATE_KEY"))
    s3.download_file(bucket_name, model_file_path, save_path)

download_model_from_s3(bucket_name,key,save_path)
