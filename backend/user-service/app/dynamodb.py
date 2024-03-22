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
                {'AttributeName': 'Email', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10},
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'EmailIndex',
                    'KeySchema': [
                        # Email will be the partition key for the GSI
                        {'AttributeName': 'Email', 'KeyType': 'HASH'}
                    ],
                    'Projection': {
                        'ProjectionType': 'KEYS_ONLY'
                    }
                }
            ]
        )
        print("EcommercePlatform table created:", response)
    except ClientError as e:
        print("Error creating EcommercePlatform table:", e)


# Function to get a user by email
# def get_user_by_email(email):
#     try:
#         response = db_users.query(
#             TableName='UserProfiles',
#             IndexName='email-index',  # Assuming 'email-index' is the name of your GSI
#             KeyConditionExpression='email = :email',
#             ExpressionAttributeValues={':email': {'S': email}}
#         )
#         items = response.get('Items', [])
#         if items:
#             return items[0]
#         else:
#             return None
#     except ClientError as e:
#         print("Error getting user by email:", e)
#         return None

# Function to add a user
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
                'Type': {'S': 'User'},
                'Email': {'S': email},
                'Password': {'S': password},
                'Username': {'S': username}
            }
        )
        print("User added with UUID:", user_uuid)
        return user_uuid
    except ClientError as e:
        print("Error adding user:", e)


def user_in_db(email):
    try:
        response = db_user_management.query(
            TableName='UserManagement',
            IndexName='EmailIndex',  # Replace with the actual name of your GSI
            KeyConditionExpression='Email = :email',
            ExpressionAttributeValues={':email': {'S': email}}
        )
        return response['Items'][0] if response['Items'] else None
    except ClientError as e:
        print(f"Error checking email existence: {e}")
        return None  # Assuming that if there's an error, the check is inconclusive


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
                'Type': {'S': 'Shop'},
                'Email': {'S': email},
                'Password': {'S': password},
                'ShopName': {'S': shop_name},
                'Address': {'S': address},
                'Phone': {'S': phone}
            }
        )
        print("Shop added with ID:", shop_uuid)
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


# Function to add dummy users
def add_dummy_data():
    dummy_users = [
        {"email": "john.doe@example.com", "password": "password1", "username": "johndoe"},
        {"email": "jane.doe@example.com", "password": "password2", "username": "janedoe"},
        {"email": "max.smith@example.com", "password": "password3", "username": "maxsmith"}
    ]
    # Adding dummy users
    for user in dummy_users:
        add_user(email=user["email"], password=user["password"], username=user["username"])

    dummy_shops = [
        {"shop_name": "John Micro", "email": "micro@example.com", "password": "password11",
         "address": "Hoferstrasse 19, Zuerich", "phone": "+41 1234567890"},
        {"shop_name": "Jane Hydro", "email": "hydro@example.com", "password": "password22",
         "address": "Bernerstrasse 18, Bern", "phone": "+41 2395678901"},
        {"shop_name": "Max Electro", "email": "electro@example.com", "password": "password33",
         "address": "Weinhofstrasse 123, Luzern", "phone": "+41 3456789012"}
    ]
    # Adding dummy shops
    for shop in dummy_shops:
        add_shop(shop_name=shop["shop_name"], email=shop["email"], password=shop["password"], address=shop["address"],
                 phone=shop["phone"])
