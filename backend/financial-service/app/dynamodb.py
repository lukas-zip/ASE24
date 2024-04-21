import boto3
import uuid
from botocore.exceptions import ClientError
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

db_accounts = boto3.client(
    "dynamodb",
    aws_access_key_id="test",  # Dummy Access Key for LocalStack
    aws_secret_access_key="test",  # Dummy Secret Key for LocalStack
    region_name="us-east-1",  # or your LocalStack configuration's region
    endpoint_url="http://localstack:4566"  # URL for LocalStack
)

# Function to create the profiles table
def create_accounts_table():
    try:
        response = db_accounts.create_table(
            TableName='Accounts',
            KeySchema=[
                {'AttributeName': 'account_id', 'KeyType': 'HASH'},
            ],
            AttributeDefinitions=[
                {'AttributeName': 'account_id', 'AttributeType': 'S'},
                {'AttributeName': 'shop_id', 'AttributeType': 'S'},
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5},
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'ShopIndex',
                    'KeySchema': [
                        # Email will be the partition key for the GSI
                        {'AttributeName': 'shop_id', 'KeyType': 'HASH'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                }
            ]
        )
        print("Finance table created:", response)
    except ClientError as e:
        print("Error creating UserManagement table:", e)

def shop_in_db(shop_id):
    try:
        response = db_accounts.query(
            TableName='Accounts',
            IndexName='ShopIndex',
            KeyConditionExpression='shop_id = :shop_id',
            ExpressionAttributeValues={':shop_id': {'S': shop_id}}
        )
        return response['Items'][0] if response['Items'] else None
    except ClientError as e:
        print(f"Error checking email existence: {e}")
        return None


# Function to add a user to the dynamodb
def add_shop_account(shop_id):
    try:
        if shop_in_db(shop_id) is not None:
            return None
        # Generate UUID for the new user
        account_uuid = str(uuid.uuid4())

        # Put the new item into the table
        db_accounts.put_item(
            TableName='Accounts',
            Item={
                'account_id': {'S': f'{account_uuid}'},
                'shop_id': {'S': shop_id},
                'balance': {'N': str(0)},
            }
        )
        print("Account added with UUID:", account_uuid)
        return account_uuid
    except ClientError as e:
        print("Error adding user:", e)


def update_balance(shop_id, amount_to_add):
    try:
        # Update the balance for the given shop_id
        amount_to_add_str = str(amount_to_add) if isinstance(amount_to_add, int) else "{:.2f}".format(amount_to_add)
        account_id = shop_in_db(shop_id).get('account_id').get('S')
        response = db_accounts.update_item(
            TableName='Accounts',
            Key={
                'account_id': {'S': account_id},
            },
            UpdateExpression='SET balance = balance + :amount',
            ExpressionAttributeValues={
                ':amount': {'N': amount_to_add_str},
            },
            ReturnValues="UPDATED_NEW"
        )
        print(f"Balance updated for shop {shop_id}. New balance: {response['Attributes']['balance']}")
        return response
    except ClientError as e:
        print(f"Error updating balance for shop {shop_id}: {e}")


# Function to get an account by UUID
def get_account_json(shop_id):
    try:
        account = shop_in_db(shop_id)
        if account is None:
            return None
        account_dict = {
            'account_id': account.get('Item', {}).get('account_id', {}).get('S', ''),
            'shop_id': account.get('Item', {}).get('shop_id', {}).get('S', ''),
            'balance': account.get('Item', {}).get('balance', {}).get('N', ''),
        }
        return account_dict
    except ClientError as e:
        print("Error getting user:", e)
