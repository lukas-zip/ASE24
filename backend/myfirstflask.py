from flask import Flask, jsonify, request
from flask_cors import CORS
import boto3
import uuid
from botocore.exceptions import ClientError

app = Flask(__name__)
CORS(app)

# Initialize AWS clients
endpoint_url = "http://localstack:4566"

db_users = boto3.client(
    "dynamodb",
    aws_access_key_id="test",
    aws_secret_access_key="test", 
    region_name="us-east-1", 
    endpoint_url=endpoint_url
)

# Function to create the profiles table
def create_profiles_table():
    try:
        response = db_users.create_table(
            TableName='UserProfiles',
            KeySchema=[
                {'AttributeName': 'profile_id', 'KeyType': 'HASH'}  # Partition key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'profile_id', 'AttributeType': 'S'}  # String
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        print("UserProfiles table created:", response)
    except ClientError as e:
        print("Error creating UserProfiles table:", e)

def create_email_index():
    try:
        response = db_users.update_table(
            TableName='UserProfiles',
            AttributeDefinitions=[
                {'AttributeName': 'email', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexUpdates=[
                {
                    'Create': {
                        'IndexName': 'email-index',
                        'KeySchema': [
                            {'AttributeName': 'email', 'KeyType': 'HASH'}
                        ],
                        'Projection': {
                            'ProjectionType': 'ALL'  # Projection type can be adjusted based on your needs
                        },
                        'ProvisionedThroughput': {
                            'ReadCapacityUnits': 5,
                            'WriteCapacityUnits': 5
                        }
                    }
                }
            ]
        )
        print("Global secondary index created:", response)
    except ClientError as e:
        print("Error creating global secondary index:", e)


# Function to add dummy users
def add_dummy_users():
    dummy_users = [
        {"email": "felix@muster.com", "password": "123"},
        {"email": "thomas@muster.com", "password": "456"}
    ]
    for user in dummy_users:
        add_user(user["email"], user["password"])

# Function to add a user
def add_user(email, password):
    try:
        # Check if the user already exists
        if get_user_by_email(email):
            print(f"User with email {email} already exists")
            return

        # Generate UUID for the new user
        user_uuid = str(uuid.uuid4())

        # Put the new item into the table
        response = db_users.put_item(
            TableName='UserProfiles',
            Item={
                'profile_id': {'S': user_uuid},  # Automatically generated UUID
                'email': {'S': email},  # User's email address
                'password': {'S': password}  # User's password (should be hashed in production)
            }
        )
        print("User added with UUID:", user_uuid)
    except ClientError as e:
        print("Error adding user:", e)

# Function to get a user by email
@app.route('/email', methods=['POST'])
def get_user_by_email(email):
    try:
        response = db_users.query(
            TableName='UserProfiles',
            IndexName='email-index',  # Assuming 'email-index' is the name of your GSI
            KeyConditionExpression='email = :email',
            ExpressionAttributeValues={':email': {'S': email}}
        )
        items = response.get('Items', [])
        if items:
            return items[0]
        else:
            return None
    except ClientError as e:
        print("Error getting user by email:", e)
        return None

@app.route('/createuser', methods=['POST'])
def create_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    try:
        # Check if the user already exists
        if get_user_by_email(email):
            print(f"User with email {email} already exists")
            return

        # Generate UUID for the new user
        user_uuid = str(uuid.uuid4())

        # Put the new item into the table
        response = db_users.put_item(
            TableName='UserProfiles',
            Item={
                'profile_id': {'S': user_uuid},  # Automatically generated UUID
                'email': {'S': email},  # User's email address
                'password': {'S': password}  # User's password (should be hashed in production)
            }
        )
        print("User added with UUID:", user_uuid)
        return jsonify({'success': 'Yayy'}), 200
    except ClientError as e:
        print("Error adding user:", e)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = get_user_by_email(email)
    #print(jsonify(user))
    if user:
        stored_password = user.get('password', {}).get('S')
        print("Stored password:", stored_password)
        print("Password provided by user:", password)
        if stored_password == password:
            return jsonify({'message': 'Login successful'}), 200
    return jsonify({'error': 'Incorrect email or password'}), 401

@app.route('/opendb', methods=['GET'])
def open_database():
    return jsonify({'message': 'Database initialized'}), 200

if __name__ == '__main__':
    create_profiles_table()
    create_email_index()
    add_dummy_users()
    app.run(host='0.0.0.0', port=5000, debug=True)
