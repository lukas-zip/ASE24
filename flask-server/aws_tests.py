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


# DynamoDB
    
# Get the service resource
dynamodb = boto3.resource('dynamodb',endpoint_url="http://localhost:4566", aws_access_key_id="test", aws_secret_access_key="test", region_name="us-east-1")

# Create the DynamoDB table

table = dynamodb.create_table(
    TableName='user',
    KeySchema=[
        {
            'AttributeName': 'username',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'last_name',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'username',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'last_name',
            'AttributeType': 'S'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists
table.wait_until_exists()

# Add items to table
table.put_item(
   Item={
        'username': 'janedoe',
        'first_name': 'Jane',
        'last_name': 'Doe',
        'age': 25,
        'account_type': 'standard_user',
    }
)

# Print out some data about the table.
print(f"Itemcount:{table.item_count}")

# Get item
response = table.get_item(
    Key={
        'username': 'janedoe',
        'last_name': 'Doe'
    }
)
item = response['Item']
print(item)

# Update item
table.update_item(
    Key={
        'username': 'janedoe',
        'last_name': 'Doe'
    },
    UpdateExpression='SET age = :val1',
    ExpressionAttributeValues={
        ':val1': 26
    }
)
# Get item
response = table.get_item(
    Key={
        'username': 'janedoe',
        'last_name': 'Doe'
    }
)
item = response['Item']
print(item)

table.delete_item(
    Key={
        'username': 'janedoe',
        'last_name': 'Doe'
    }
)

# Print out some data about the table.
print(f"Itemcount:{table.item_count}")

# Detete Table
table.delete()

# Batch create items & batch update is possible
# Scaning possible based on attributes or conditions