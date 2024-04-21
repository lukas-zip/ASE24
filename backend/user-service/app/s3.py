import boto3
import uuid
from botocore.exceptions import ClientError


db_s3_user_management_pictures = boto3.client(
    "s3",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1",
    endpoint_url="http://localstack:4566"
)

# ------------------------------------------
# Database for pictures --> S3
# ------------------------------------------

def create_bucket(bucket_name):
    try:
        db_s3_user_management_pictures.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' created successfully.")
    except ClientError as e:
        print(f"Error creating bucket '{bucket_name}': {e}")

def upload_fileobj(image_file, bucket_name, object_key):
    try:
        db_s3_user_management_pictures.upload_fileobj(image_file, bucket_name, object_key)
        return True
    except ClientError as e:
        print("Error uploading file to S3:", e)
        return False

def bucket_exists(bucket_name):
    try:
        db_s3_user_management_pictures.head_bucket(Bucket=bucket_name)
        return True
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            return False
        else:
            print(f"Error checking bucket existence: {e}")
            return False

def delete_object(object_key, bucket_name):
    #modifiedobject_key = f'{object_key}.jpg'
    try:
        db_s3_user_management_pictures.delete_object(Bucket=bucket_name, Key=object_key)
        print(f"Object '{object_key}' deleted successfully from bucket '{bucket_name}'.")
        return True
    except ClientError as e:
        print(f"Error deleting object '{object_key}' from bucket '{bucket_name}': {e}")
        return False

def retrieve_image(object_key, bucket_name):
    try:
        # Get the object from S3
        response = db_s3_user_management_pictures.get_object(Bucket=bucket_name, Key=object_key)

        # Read the image data
        image_data = response['Body'].read()

        return image_data
    except ClientError as e:
        print(f"Error retrieving object '{object_key}' from bucket '{bucket_name}': {e}")
        return None