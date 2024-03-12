import boto3
import logging
import json
import os
from botocore.exceptions import ClientError 
from flask import Flask, jsonify, request

# from flask import Flask, flash, request, redirect, render_template, session
# import os

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return "<p>Hello, this works!</p>"

# if __name__ == "__main__":
#     port = int(os.environ.get('PORT', 5300)) #Hier muss der Port stehen
#     app.run(debug=True, host='0.0.0.0', port=port)

app = Flask (__name__)
# Determine endpoint URL based on environment variable
endpoint_url = os.environ.get("S3_ENDPOINT_URL", "http://localstack:4566")

s3 = boto3.client(
    "s3",
    aws_access_key_id="test",
    aws_secret_access_key="test", 
    region_name="us-east-1", 
    endpoint_url=endpoint_url,
)

#boto3.setup_default_session(profile_name='localstack')

#logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')

def create_bucket(bucketname):
    try:
        response = s3.create_bucket(
            Bucket = bucketname
        )
    except ClientError:
        logger.exception('Could not create S3 bucket locally.')
        raise
    else:
        return response

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    try:
        bucket_name = "hands-on-cloud-localstack-bucket"  # Ensure consistency with the bucket name
        acl = "private"  # Specify ACL if required
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,  # Use the file's original filename as the object key
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type,  # Set appropriate content type as per the file
            },
        )
    except ClientError as e:
        return jsonify({"message": f"Failed ({e})"})
    return jsonify({"message": "File uploaded successfully!"})

@app.route('/objects', methods=["GET"])
def list_objects():
    try:
        response = s3.list_objects(Bucket="hands-on-cloud-localstack-bucket")
        objects = [obj["Key"] for obj in response.get("Contents", [])]
        return jsonify({"objects": objects})
    except ClientError as e:
        return jsonify({"error": f"Failed to list objects: {e}"}), 500

@app.route('/')
def home():
    return "<p>Hello, this works!</p>"

def main():
    bucket_name = "hands-on-cloud-localstack-bucket"
    logger.info('Creating S3 bucket locally using LocalStack')
    so3 = create_bucket(bucket_name)
    logger.info('S3 bucket created.')
    logger.info(json.dumps(so3, indent=4) + '\n')

if __name__ == "__main__":
    #port = int(os.environ.get('PORT', 5300))
    main()
    app.run(debug=True, host="0.0.0.0")