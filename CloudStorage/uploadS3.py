import logging
import boto3
from botocore.exceptions import ClientError
from datetime import datetime

def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

timestamp = datetime.now().timestamp()

print(upload_file('TomatoTracker/CloudStorage/image.jpg', 'tomato-tracker-images', f'image-{timestamp}.jpg'))