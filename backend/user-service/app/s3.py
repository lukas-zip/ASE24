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
    """
    Creates an S3 bucket with the specified name using the Boto3 S3 client.

    :param bucket_name: The name of the bucket to create.
    :return: None, prints success or error message.
    :raises ClientError: If there's an error during the bucket creation process.
    """
    try:
        db_s3_user_management_pictures.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' created successfully.")
    except ClientError as e:
        print(f"Error creating bucket '{bucket_name}': {e}")

def upload_fileobj(image_file, bucket_name, object_key):
    """
    Uploads a file object to an S3 bucket at the specified object key.

    :param image_file: The file-like object to upload.
    :param bucket_name: The name of the S3 bucket where the file will be uploaded.
    :param object_key: The key under which the file object will be stored.
    :return: True if the upload is successful, False otherwise.
    :raises ClientError: If there's an error during the file upload process.
    """
    try:
        db_s3_user_management_pictures.upload_fileobj(image_file, bucket_name, object_key)
        return True
    except ClientError as e:
        print("Error uploading file to S3:", e)
        return False

def bucket_exists(bucket_name):
    """
    Checks if an S3 bucket exists by attempting to retrieve its metadata.

    :param bucket_name: The name of the bucket to check.
    :return: True if the bucket exists, False if the bucket does not exist or an error occurs.
    :raises ClientError: If an unexpected error occurs during the check (other than 404 not found).
    """
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
    """
    Deletes an object from an S3 bucket.

    :param object_key: The key of the object to delete.
    :param bucket_name: The name of the bucket from which the object will be deleted.
    :return: True if the object is successfully deleted, False otherwise.
    :raises ClientError: If there's an error during the deletion process.
    """
    try:
        db_s3_user_management_pictures.delete_object(Bucket=bucket_name, Key=object_key)
        print(f"Object '{object_key}' deleted successfully from bucket '{bucket_name}'.")
        return True
    except ClientError as e:
        print(f"Error deleting object '{object_key}' from bucket '{bucket_name}': {e}")
        return False

def retrieve_image(object_key, bucket_name):
    """
    Retrieves image data from an S3 bucket at the specified object key.

    :param object_key: The key of the object to retrieve.
    :param bucket_name: The name of the bucket from which the object is retrieved.
    :return: The image data as a bytes object if successful, None otherwise.
    :raises ClientError: If there's an error retrieving the object.
    """
    try:
        # Get the object from S3
        response = db_s3_user_management_pictures.get_object(Bucket=bucket_name, Key=object_key)

        # Read the image data
        image_data = response['Body'].read()

        return image_data
    except ClientError as e:
        print(f"Error retrieving object '{object_key}' from bucket '{bucket_name}': {e}")
        return None