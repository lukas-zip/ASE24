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



# app = Flask (__name__)
# # Determine endpoint URL based on environment variable


# #boto3.setup_default_session(profile_name='localstack')

# #logger config
# logger = logging.getLogger()
# logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')

# def create_bucket(bucketname):
#     try:
#         response = s3.create_bucket(
#             Bucket = bucketname
#         )
#     except ClientError:
#         logger.exception('Could not create S3 bucket locally.')
#         raise
#     else:
#         return response

# @app.route("/upload", methods=["POST"])
# def upload_file():
#     file = request.files["file"]
#     try:
#         bucket_name = "hands-on-cloud-localstack-bucket"  # Ensure consistency with the bucket name
#         acl = "private"  # Specify ACL if required
#         s3.upload_fileobj(
#             file,
#             bucket_name,
#             file.filename,  # Use the file's original filename as the object key
#             ExtraArgs={
#                 "ACL": acl,
#                 "ContentType": file.content_type,  # Set appropriate content type as per the file
#             },
#         )
#     except ClientError as e:
#         return jsonify({"message": f"Failed ({e})"})
#     return jsonify({"message": "File uploaded successfully!"})

# @app.route('/objects', methods=["GET"])
# def list_objects():
#     try:
#         response = s3.list_objects(Bucket="hands-on-cloud-localstack-bucket")
#         objects = [obj["Key"] for obj in response.get("Contents", [])]
#         return jsonify({"objects": objects})
#     except ClientError as e:
#         return jsonify({"error": f"Failed to list objects: {e}"}), 500

# @app.route('/')
# def home():
#     return "<p>Hello, this works!</p>"

# def main():
#     bucket_name = "hands-on-cloud-localstack-bucket"
#     logger.info('Creating S3 bucket locally using LocalStack')
#     so3 = create_bucket(bucket_name)
#     logger.info('S3 bucket created.')
#     logger.info(json.dumps(so3, indent=4) + '\n')

# if __name__ == "__main__":
#     #port = int(os.environ.get('PORT', 5300))
#     main()
#     app.run(debug=True, host="0.0.0.0")


#     # from flask import Flask, flash, request, redirect, render_template, session
# # import os

# # app = Flask(__name__)

# # @app.route('/')
# # def home():
# #     return "<p>Hello, this works!</p>"

# # if __name__ == "__main__":
# #     port = int(os.environ.get('PORT', 5300)) #Hier muss der Port stehen
# #     app.run(debug=True, host='0.0.0.0', port=port)