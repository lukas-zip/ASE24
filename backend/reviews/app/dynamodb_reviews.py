import boto3
import uuid
from botocore.exceptions import ClientError

# Initialize dynamoDB 
db_reviews = boto3.client(
    "dynamodb_rieview",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1",
    endpoint_url="http://localstack:4566"
)


# Function to create the reviews table
def create_review_tables():
    try:
        response = db_reviews.create_table(
            TableName='Reviews',
            KeySchema=[
                {'AttributeName': 'PK', 'KeyType': 'HASH'},
                {'AttributeName': 'SK', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'PK', 'AttributeType': 'S'},
                {'AttributeName': 'SK', 'AttributeType': 'S'},
                {'AttributeName': 'customer_id', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10},
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'CustomerIndex',
                    'KeySchema': [
                        # Customer_ID will be the partition key for the GSI
                        {'AttributeName': 'customer_id', 'KeyType': 'HASH'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                }
            ]
        )
        print("ReviewManagement table created:", response)
    except ClientError as e:
        print("Error creating ReviewManagement table:", e)


# Function to add a review to the dynamodb
def add_review(product_id,customer_id,reviewcontent,rating,time_lastedit,time_created):
    try:
        if review_in_db(product_id,customer_id) is not None:
            return {'error': 'Customer already added a review for this product'}

        # Generate UUID for the new user
        review_uuid = str(uuid.uuid4())

        # Put the new item into the table
        response = db_reviews.put_item(
            TableName='Reviews',
            Item={
                'PK': {'S': f'Review#{review_uuid}'},
                'SK': {'S': product_id},
                'customer_id': {'S': customer_id},
                'reviewcontent': {'S': reviewcontent},
                'rating': {'S': rating},
                'time_lastedit': {'S': time_lastedit},
                'time_created': {'S': time_created}
            }
        )
        print("Review added with UUID:", review_uuid)
        return review_uuid
    except ClientError as e:
        print("Error adding review:", e)

def delete_review(review_uuid):
    return None

def edit_review(review_uuid):
    return None

# Function to get all reviews by product ID for display??
## change
def get_user(user_uuid):
    try:
        response = db_reviews.get_item(
            TableName='UserManagement',
            Key={
                'PK': {'S': f'USER#{user_uuid}'},
                'SK': {'S': f'PROFILE#{user_uuid}'}
            }
        )
        return response.get('Item')
    except ClientError as e:
        print("Error getting user:", e)

# Fuction to check if the customer has already made a review of the product
## change to customer and product already there
def review_in_db(customer_id,product_id):
    try:
        response = db_reviews.query(
            TableName='ReviewManagement',
            IndexName='CustomerIndex',
            KeyConditionExpression='customer_id = :customer_id',
            ExpressionAttributeValues={':customer_id': {'S': customer_id}}
        )
        return response['Items'][0] if response['Items'] else None
    except ClientError as e:
        print(f"Error Review from customer already exists: {e}")
        return None  # Assuming that if there's an error, the check is inconclusive


