import boto3
import uuid
from botocore.exceptions import ClientError
import os
from werkzeug.utils import secure_filename
from botocore.exceptions import ClientError
from flask import Flask, Response
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

db_user_management = boto3.client(
    "dynamodb",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1",
    endpoint_url="http://localstack:4566"
)
s3_client = boto3.client(
    "s3",
    aws_access_key_id="test",  # Dummy Access Key
    aws_secret_access_key="test",  # Dummy Secret Key
    region_name="us-east-1",  # or your LocalStack configuration's region
    endpoint_url="http://localstack:4566"  # URL for LocalStack (adjust if using a different port)
)

# Create S3 bucket on LocalStack
def create_s3_bucket():
    try:
        bucket_name = 'userview'
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} created successfully.")
    except ClientError as e:
        print(f"Error creating bucket: {e}")


# Function to create the profiles table
def create_user_management_tables():
    try:
        response = db_user_management.create_table(
            TableName='UserManagement',
            KeySchema=[
                {'AttributeName': 'PK', 'KeyType': 'HASH'},
                {'AttributeName': 'SK', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'PK', 'AttributeType': 'S'},
                {'AttributeName': 'SK', 'AttributeType': 'S'},
                {'AttributeName': 'email', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10},
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'EmailIndex',
                    'KeySchema': [
                        # Email will be the partition key for the GSI
                        {'AttributeName': 'email', 'KeyType': 'HASH'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                }
            ]
        )
        print("UserManagement table created:", response)
    except ClientError as e:
        print("Error creating UserManagement table:", e)


# Function to add a user to the dynamodb
def add_user(email, password, username):
    try:
        if user_in_db(email) is not None:
            return {'error': 'Email already in use by a different profile'}

        # Generate UUID for the new user
        user_uuid = str(uuid.uuid4())

        # Put the new item into the table
        db_user_management.put_item(
            TableName='UserManagement',
            Item={
                'PK': {'S': f'USER#{user_uuid}'},
                'SK': {'S': f'PROFILE#{user_uuid}'},
                'type': {'S': 'User'},
                'profile_picture': {'S': "NONE"},
                'email': {'S': email},
                'username': {'S': username},
                'password': {'S': password}
            }
        )
        print("User added with UUID:", user_uuid)
        return user_uuid
    except ClientError as e:
        print("Error adding user:", e)


# Function to get a user by UUID
def get_user(user_uuid):
    try:
        response = db_user_management.get_item(
            TableName='UserManagement',
            Key={
                'PK': {'S': f'USER#{user_uuid}'},
                'SK': {'S': f'PROFILE#{user_uuid}'}
            }
        )
        return response.get('Item')
    except ClientError as e:
        print("Error getting user:", e)


def user_in_db(email):
    try:
        response = db_user_management.query(
            TableName='UserManagement',
            IndexName='EmailIndex',
            KeyConditionExpression='email = :email',
            ExpressionAttributeValues={':email': {'S': email}}
        )
        return response['Items'][0] if response['Items'] else None
    except ClientError as e:
        print(f"Error checking email existence: {e}")
        return None  # Assuming that if there's an error, the check is inconclusive


# Function to add a shop to the dynamodb
def add_shop(shop_name, email, password, address, phone):
    try:
        # Check if the user already exists
        if user_in_db(email):
            print(f"Email already in use by a different profile")
            return

        # Generate UUID for the new user
        shop_uuid = str(uuid.uuid4())

        # Put the new item into the table
        response = db_user_management.put_item(
            TableName='UserManagement',
            Item={
                'PK': {'S': f'SHOP#{shop_uuid}'},
                'SK': {'S': f'DETAILS#{shop_uuid}'},
                'type': {'S': 'Shop'},
                'email': {'S': email},
                'password': {'S': password},
                'shop_name': {'S': shop_name},
                'address': {'S': address},
                'phone': {'S': phone}
            }
        )
        print("Shop added with UUID:", shop_uuid)
        return shop_uuid
    except ClientError as e:
        print("Error adding shop:", e)


# Function to get a shop by ID
def get_shop(shop_uuid):
    """
    Retrieve a shop's details from the DynamoDB table based on its UUID.

    :param shop_uuid: The UUID of the shop to retrieve.
    :return: A dictionary representing the shop item if found, None otherwise.
    """
    try:
        response = db_user_management.get_item(
            TableName='UserManagement',
            Key={
                'PK': {'S': f'SHOP#{shop_uuid}'},
                'SK': {'S': f'DETAILS#{shop_uuid}'}
            }
        )
        return response.get('Item')
    except ClientError as e:
        print("Error getting shop:", e)


def get_entity(entity_uuid):
    """
    Fetch an entity (user or shop) from the DynamoDB table using the entity UUID.

    :param entity_uuid: The UUID of the entity to fetch.
    :return: The entity item if found, None otherwise.
    """
    try:
        # Attempt to fetch the user
        user_response = get_user(entity_uuid)
        if user_response is not None and 'Item' in user_response:
            return user_response['Item']

        # If not found, attempt to fetch the shop
        shop_response = get_shop(entity_uuid)
        if shop_response is not None and 'Item' in shop_response:
            return shop_response['Item']
        # If no entity is found, return None
        return None
    except ClientError as e:
        print("Error getting entity:", e)


# Uploads a profile picture to S3 and updates the user's DynamoDB entry.
def update_profile_picture(entity_uuid, file_path, filename):
    try:
        bucket_name = 'userview'
        s3_client.upload_file(file_path, bucket_name, f"{entity_uuid}/{filename}")
        image_url = f"http://{bucket_name}.s3.localhost.localstack.cloud:4566/{entity_uuid}/{filename}"

        # Determine the prefix based on the entity type
        entity_type = get_user(entity_uuid)['type']
        prefix = 'USER#' if entity_type.get('S') == 'User' else 'SHOP#'

        # Update the item in the table to include the profile picture URL
        response = db_user_management.update_item(
            TableName='UserManagement',
            Key={
                'PK': {'S': f'{prefix}{entity_uuid}'},
                'SK': {'S': f'PROFILE#{entity_uuid}' if entity_type.get('S') == 'User' else f'DETAILS#{entity_uuid}'},
            },
            UpdateExpression='SET profile_picture = :val',
            ExpressionAttributeValues={
                ':val': {'S': image_url}
            },
            ReturnValues="UPDATED_NEW"
        )
        print(f"{entity_type} profile picture updated:", response)
        return response
    except ClientError as e:
        print(f"Error updating profile picture:", e)
