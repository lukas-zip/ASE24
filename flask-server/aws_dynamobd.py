import boto3

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
#item = response['Item']
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