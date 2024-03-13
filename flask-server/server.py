from flask import Flask, jsonify
from botocore.exceptions import ClientError
import boto3
import os

app = Flask(__name__)

#endpoint
endpoint_url = os.environ.get("S3_ENDPOINT_URL","http://localhost:4566")

s3 = boto3.client('s3', endpoint_url=endpoint_url, aws_access_key_id="test", aws_secret_access_key="test", region_name="us-east-1")

#@app.route("/members") -> klappt nicht mit members...
@app.route("/upload")
def upload_file():
    responseobjects = []
    try:
        s3.create_bucket(Bucket= "ase")
        s3.upload_file(r'C:\Users\lena-\Documents\Master\UZH\FS24\AdvancedSoftwareEngineering\rplusf\flask-server\testfile.text','ase','testfile.txt')
        
        # List Objects in Buckets
        response = s3.list_objects(Bucket='ase')

        # Iterate over the objects in the response
        if 'Contents' in response:
            for obj in response['Contents']:
                responseobjects.append(obj['Key'])
        else:
            responseobjects = responseobjects.append('No objects found in the bucket')
    except ClientError as e:
        return jsonify({"message":f"Failed ({e})"})
    return jsonify({"message":f"File uploaded successfully, Files in Bucket: {responseobjects}"})



if __name__ == "__main__":
    app.run()
    #app.run(host="0.0.0.0")