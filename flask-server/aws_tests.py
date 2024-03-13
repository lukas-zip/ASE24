import boto3

# S3

# Initialize boto3 client
#s3_client = boto3.client('s3', endpoint_url="http://localhost:4566", aws_access_key_id="test", aws_secret_access_key="test")

# Create bucket
#s3_client.create_bucket(Bucket="test-bucket-01", CreateBucketConfiguration={'LocationConstraint':'eu-west-1'})

# List buckets
#response = s3_client.list_buckets()
#print(response)

# Upload file, r converts a normal string to a raw string
#s3_client.upload_file(r'C:\Users\lena-\Documents\Master\UZH\FS24\AdvancedSoftwareEngineering\rplusf\flask-server\testfile.text','test-bucket-01','testfile.txt')

# List Objects in Buckets
#response = s3_client.list_objects(Bucket='test-bucket-01')

# Iterate over the objects in the response
#if 'Contents' in response:
#    for obj in response['Contents']:
#        print('Object Key:', obj['Key'])
#else:
#   print('No objects found in the bucket.')

#responseobjects = []
#if 'Contents' in response:
#    for obj in response['Contents']:
#        responseobjects.append(obj['Key'])
#else:
#    responseobjects = responseobjects.append('No objects found in the bucket')
#print(responseobjects)


