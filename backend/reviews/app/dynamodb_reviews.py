import boto3
import uuid
from botocore.exceptions import ClientError
from app import dummydata_reviews
import json
from datetime import datetime
import requests

# Initialize dynamoDB 
db_reviews = boto3.client(
    "dynamodb",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1",
    endpoint_url="http://localstack:4566"
)

def get_dynamodb():
    return db_reviews

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
def add_review(product_id,customer_id,reviewcontent,rating):
    try:
        value, status = check_review(customer_id,product_id)
        if status:

            # Generate UUID for the review 
            review_uuid = str(uuid.uuid4())

            time_lastedit = datetime.now()
            time_lastedit = time_lastedit.strftime('%a %d %b %Y, %I:%M%p')
            time_created = datetime.now()
            time_created = time_created.strftime('%a %d %b %Y, %I:%M%p')

            # Put the new item into the table
            response = db_reviews.put_item(
                TableName='Reviews',
                Item={
                    'PK': {'S': review_uuid},
                    'SK': {'S': product_id},
                    'customer_id': {'S': customer_id},
                    'reviewcontent': {'S': reviewcontent},
                    'rating': {'N': rating},
                    'time_lastedit': {'S': time_lastedit},
                    'time_created': {'S': time_created}
                }
            )
            print("Review added with UUID:", review_uuid)
            return "Successfully added Review", True
        
        else:
            return "Customer already added a review for this product", False
    except ClientError as e:
        print("Error adding review:", e)

# Fuction to delete item from dynamo DB
def delete_review(review_uuid,product_id,user_id):
    # check if review belongs to the customer deleting it
    response_data, status = get_review(review_uuid,product_id)
    response_review = response_data[0]
    customer_id = response_review['customer_id']
    if user_id == customer_id:
        # delete review
        try:
            response = db_reviews.delete_item(
                    TableName='Reviews',
                    Key={
                        'PK': {'S':review_uuid},
                        'SK': {'S':product_id}
                        }
            )
            response_data, status = get_review(review_uuid,product_id)
            if response_data == []:
                return 'Successfully deleted Review!',True
            else:
                return "Review not deleted successfully", False
        except Exception as e:
            print("Error deleting review:", e)
            raise e
    else: 
        return "The review does not belong to this user", False
    
#edit a review that has already been made
def edit_review(review_uuid,product_id, user_id,reviewcontent,rating):
    # check if review belongs to the customer editing it
    response_data, status = get_review(review_uuid,product_id)
    if response_data != []:
        response_review = response_data[0]
        customer_id = response_review['customer_id']
        if user_id == customer_id:
            try:
                time_lastedit = datetime.now()
                time_lastedit = time_lastedit.strftime('%a %d %b %Y, %I:%M%p')
                # Put the new item into the table
                response = db_reviews.update_item(
                    TableName='Reviews',
                    Key={
                        'PK': {'S':review_uuid},
                        'SK': {'S':product_id}
                        },
                    UpdateExpression='SET reviewcontent = :r, rating = :t, time_lastedit = :l',
                    ExpressionAttributeValues={
                        ':r': {'S': reviewcontent},
                        ':t': {'N': rating},
                        ':l': {'S': time_lastedit}
                    }
                )
                print("Review updated with UUID:", review_uuid)
                return get_review(review_uuid,product_id)
            except ClientError as e:
                print("Error updating review:", e)
                return None
        else:
            return "The review does not belong to this user", False
    else: 
        return "The review does not exist", False

# Fuction to check if the customer has already made a review for the product
def check_review(customer_id,product_id):
    try:
        response = db_reviews.scan(
            TableName='Reviews',
            FilterExpression='SK = :sk AND customer_id = :cid',
            ExpressionAttributeValues={
                ':cid': {'S':customer_id},
                ':sk': {'S':product_id}
                }
            )
        if len(response['Items']) < 1:
            return "Customer has not jet made a review for this product",True
        else:
            return "Review already exists", False

    except ClientError as e:
        print(f"Error Review from customer already exists: {e}")
        return "Error getting review!", e  

# Function to get reviews by reviewID
def get_review(review_uuid,product_id):
    try:
        response = db_reviews.get_item(
            TableName='Reviews',
            Key={
                'PK': {'S':review_uuid},
                'SK': {'S':product_id}
            }
        )
        if len(response) > 1:
            item = response['Item']
            formatted_review = []
            user_id = item.get('customer_id', {}).get('S')
            response_json= requests.get(f'http://user-service:8001/users/{user_id}')
            response_user = response_json.json()
            review = {
                "review_id": item.get('PK', {}).get('S'),
                "product_id": product_id,
                "customer_id": item.get('customer_id', {}).get('S'),
                "reviewcontent": item.get('reviewcontent', {}).get('S'),
                "rating": item.get('rating', {}).get('N'),
                "time_lastedit": item.get('time_lastedit', {}).get('S'),
                "time_created": item.get('time_created', {}).get('S'),
                "customer": response_user['value']
            }
            formatted_review.append(review)
            return formatted_review, True
        else:
            return [], False
    except ClientError as e:
        print("Error getting review:", e)
        return "Error getting review!", e

# Get all the reviews to a product
def get_batch(product_id):
    try:
        response = db_reviews.scan(
            TableName='Reviews',
            FilterExpression='SK = :sk',
            ExpressionAttributeValues={
                ':sk': {'S':product_id}
                }
            )
        if len(response['Items']) > 0:
            items = response.get('Items', [])
            formatted_review = []
            for item in items:
                user_id = item.get('customer_id', {}).get('S')
                response_json= requests.get(f'http://user-service:8001/users/{user_id}')
                response_user = response_json.json()
                review = {
                    "review_id": item.get('PK', {}).get('S'),
                    "product_id": product_id,
                    "customer_id": item.get('customer_id', {}).get('S'),
                    "reviewcontent": item.get('reviewcontent', {}).get('S'),
                    "rating": item.get('rating', {}).get('N'),
                    "time_lastedit": item.get('time_lastedit', {}).get('S'),
                    "time_created": item.get('time_created', {}).get('S'),
                    "customer": response_user['value']
                }
                formatted_review.append(review)
            return formatted_review, True
        else:
            return [], False
    except ClientError as e:
        print("Error getting review:", e)
        return "Error getting review!", e

## delete review tabele
def delete_review_tables():
    try:
        db_reviews.delete_table(TableName='Reviews')
    except db_reviews.exceptions.ResourceNotFoundException:
        print("Table does not exist.")