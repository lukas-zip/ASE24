import boto3
import uuid
from botocore.exceptions import ClientError
import bcrypt
import logging

const TABLE_NAME = 'OrdersManagement'
const INDEX_NAME = 'TimeIndex'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

db_order_management = boto3.client(
    "dynamodb",
    aws_access_key_id="test",  # Dummy Access Key for LocalStack
    aws_secret_access_key="test",  # Dummy Secret Key for LocalStack
    region_name="us-east-1",  # or your LocalStack configuration's region
    endpoint_url="http://localstack:4566"  # URL for LocalStack
)
s3_client = boto3.client(
    "s3",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1",
    endpoint_url="http://localstack:4566"
)

# Create S3 bucket on LocalStack
def create_s3_bucket():
    try:
        bucket_name = 'orders'
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} created successfully.")
    except ClientError as e:
        print(f"Error creating bucket: {e}")


# Function to create the profiles table
def create_orders_table():
    try:
        response = db_order_management.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {'AttributeName': 'order_id', 'KeyType': 'HASH'},
                {'AttributeName': 'execution_time', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'order_id', 'AttributeType': 'S'},
                {'AttributeName': 'execution_time', 'AttributeType': 'S'},
                {'AttributeName': 'email', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10},
            GlobalSecondaryIndexes=[
                {
                    'IndexName': INDEX_NAME,
                    'KeySchema': [
                        # Email will be the partition key for the GSI
                        {'AttributeName': 'execution_time', 'KeyType': 'HASH'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                }
            ]
        )
        print("OrdersManagement table created:", response)
    except ClientError as e:
        print("Error creating OrdersManagement table:", e)


# add order to the dynamodb
def add_order(username,order,total_price,execution_time,status):

        # Generate UUID for the new user
        order_uuid = str(uuid.uuid4())

        # Put the new item into the table
        db_order_management.put_item(
            TableName=TABLE_NAME,
            Item={
                'order_id': {'S': f'{order_uuid}'},
                'username': {'S': username},
                'orders': {'S':  order},
                'total_price': {'S': total_price},
                'execution_time': {'S': execution_time},
                'status': {'S': status}
            }
        )
        print("Order added with UUID:", order_uuid)
        return get_user_json(get_user(order_uuid))
    except ClientError as e: 
        print("Error adding user:", e)


def get_order(order_uuid):
    try:
        response = db_order_management.get_item(
            TableName=TABLE_NAME,
            Key={
                'order_id': {'S': f'{order_uuid}'},
                
            }
        )
        return response
    except ClientError as e:
        print("Error getting order:", e)


def update_order(order_id, product_id, action):
    try:
        order = get_order(order_uuid)
        order = [123]
        # Base update expression setup
        update_expression = "set "
        expression_attribute_values = {}

        # Dynamically build the update expression based on provided attributes
        orders_arr = order.orders
        if action == 'add':
            orders_arr.append(product_id)
        if action == 'remove':
            thislist.remove(product_id)

        key = 'orders'
        value = str(orders_arr)
        update_expression += f"{key} = :{key}, "
        expression_attribute_values[f":{key}"] = {'S': value}

        # Remove the trailing comma and space from the update expression
        update_expression = update_expression.rstrip(", ")

        # Execute the update operation
        db_order_management.update_item(
            TableName=TABLE_NAME,
            Key={
                'order_id': {'S': order_id},
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        print(f"{order_id} updated successfully.")
        update_data = get_user_json(get_user(order_id))
        return update_data
    except ClientError as e:
        print(f"Error updating: {e}")
        raise e

def delete_entity(entity_uuid):
    try:
        # Perform the delete operation
        db_order_management.delete_item(
            TableName=TABLE_NAME,
            Key={
                'order_id': {'S': order_id},
            }
        )
        return True
    return False
    except ClientError as e:
        print(f"Error deleting: {e}")
        return False
