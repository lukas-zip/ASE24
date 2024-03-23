import boto3
import uuid
from botocore.exceptions import ClientError

db_user_management = boto3.client(
    "dynamodb",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1",
    endpoint_url="http://localstack:4566"
)


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
        response = db_user_management.put_item(
            TableName='UserManagement',
            Item={
                'PK': {'S': f'USER#{user_uuid}'},
                'SK': {'S': f'PROFILE#{user_uuid}'},
                'type': {'S': 'User'},
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
        if get_user(email):
            print(f"User with email {email} already exists")
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
def get_shop(shop_id):
    try:
        response = db_user_management.get_item(
            TableName='UserManagement',
            Key={
                'PK': {'S': f'SHOP#{shop_id}'},
                'SK': {'S': f'DETAILS#{shop_id}'}
            }
        )
        return response.get('Item')
    except ClientError as e:
        print("Error getting shop:", e)
