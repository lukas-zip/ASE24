from flask import Flask, jsonify, request
import boto3
import os
from botocore.exceptions import ClientError

app = Flask(__name__)

#os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'  # Replace 'us-east-1' with your desired region
endpoint_url = "http://localstack:4566"

cognito_client = boto3.client(
    "cognito-idp",
    aws_access_key_id="test",
    aws_secret_access_key="test", 
    region_name="us-east-1", 
    endpoint_url=endpoint_url,
)

iam_client = boto3.client(
    "iam",
    aws_access_key_id="test",
    aws_secret_access_key="test", 
    region_name="us-east-1", 
    endpoint_url=endpoint_url,
)

# Initialize AWS clients
#iam_client = boto3.client("iam", endpoint_url="http://localhost:4566")
#cognito_client = boto3.client("cognito-idp", endpoint_url="http://localhost:4566")

def create_dummy_user(username, password):
    try:
        response = cognito_client.admin_create_user(
            UserPoolId='<your-user-pool-id>',
            Username=username,
            TemporaryPassword=password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': f'{username}@example.com'
                },
                # Add additional user attributes here if needed
            ],
            MessageAction='SUPPRESS'
        )
        return True
    except ClientError as e:
        print("Error creating dummy user:", e)
        return False

def insert_dummy_users():
    users = [
        {'username': 'johndoe@johndoe.com', 'password': '123'},
        {'username': 'mustermann@mustermann.com', 'password': '456'},
    ]
    for user in users:
        create_dummy_user(user['username'], user['password'])

# Create a route to trigger the insertion of dummy users
@app.route('/insert_dummy_users', methods=['GET'])
def trigger_insert_dummy_users():
    insert_dummy_users()
    return jsonify({'message': 'Dummy users inserted successfully'}), 200

@app.route('/login', methods=['POST'])
def login():
     # Parse username and password from request body
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Check if username and password are provided
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    try:
        # Authenticate user using Cognito
        response = cognito_client.initiate_auth(
            ClientId='<your-client-id>',
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )

        # Extract tokens from response
        access_token = response['AuthenticationResult']['AccessToken']
        id_token = response['AuthenticationResult']['IdToken']

        # Return tokens or any other information you need
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'id_token': id_token
        }), 200

    except ClientError as e:
        # Handle authentication errors
        if e.response['Error']['Code'] == 'NotAuthorizedException':
            return jsonify({'error': 'Incorrect username or password'}), 401
        elif e.response['Error']['Code'] == 'UserNotFoundException':
            return jsonify({'error': 'User not found'}), 404
        else:
            return jsonify({'error': 'Authentication failed'}), 401

if __name__ == '__main__':
    insert_dummy_users()

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