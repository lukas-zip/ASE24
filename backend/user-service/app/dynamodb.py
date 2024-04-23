import boto3
import uuid
from botocore.exceptions import ClientError
import bcrypt
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def get_dynamodb_resource():
    s3_client = boto3.client(
        "s3",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1",
        endpoint_url="http://localstack:4566"
    )
    dynamodb = boto3.client(
        "dynamodb",
        aws_access_key_id="test",  # Dummy Access Key for LocalStack
        aws_secret_access_key="test",  # Dummy Secret Key for LocalStack
        region_name="us-east-1",  # or your LocalStack configuration's region
        endpoint_url="http://localstack:4566"  # URL for LocalStack
    )
    return dynamodb, s3_client


db_user_management, s3_client = get_dynamodb_resource()


# Create S3 bucket on LocalStack
def create_s3_bucket():
    try:
        bucket_name = 'userview'
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} created successfully.")
    except ClientError as e:
        print(f"Error creating bucket: {e}")


# Function to create the profiles table
def create_user_management_tables(dynamodb=db_user_management):
    try:
        response = dynamodb.create_table(
            TableName='UserManagement',
            KeySchema=[
                {'AttributeName': 'PK', 'KeyType': 'HASH'},
                {'AttributeName': 'SK', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'PK', 'AttributeType': 'S'},
                {'AttributeName': 'SK', 'AttributeType': 'S'},
                {'AttributeName': 'email', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10},
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'EmailIndex',
                    'KeySchema': [
                        # Email will be the partition key for the GSI
                        {'AttributeName': 'email', 'KeyType': 'HASH'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                }
            ]
        )
        print("UserManagement table created:", response)
        return response
    except ClientError as e:
        print("Error creating UserManagement table:", e)

def delete_user_management_tables():
    db_user_management.delete_table(TableName='UserManagement')

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_login(email, password):
    """
    Verify if the provided password matches the hashed password stored in DynamoDB.

    :param email: The email of the user, used to retrieve the user's data from DynamoDB.
    :param password: The password to be verified.
    :return: True if the password is correct, False otherwise.
    """
    try:
        # Retrieve the user data based on the email
        entity = user_in_db(email)
        if entity is None:
            return False  # User not found
        stored_hashed_password = entity['password'].get('S').encode('utf-8')
        # Compare the provided password with the stored hashed password
        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
            entity_uuid = entity['PK'].get('S')[5:]
            return get_user_json(get_user(entity_uuid)) if entity['type'].get('S') == 'User' else get_shop_json(get_shop(entity_uuid))
        return False
    except ClientError as e:
        print(f"An error occurred: {e}")
        return False


def change_password(entity_uuid, old_password, new_password):
    # Retrieve the user's current password hash from DynamoDB
    entity = get_entity(entity_uuid)

    if not entity:
        print('Entity not found')
        return False

    entity = entity.get('Item')
    entity_type = entity['type'].get('S')
    stored_hashed_password = entity['password'].get('S').encode('utf-8')

    # Verify the old password
    if not bcrypt.checkpw(old_password.encode('utf-8'), stored_hashed_password):
        return "mismatch"

    # Hash the new password and update in DynamoDB
    new_password_hash = hash_password(new_password)
    pk_value, sk_value = pk_sk_values(entity_uuid)

    try:
        db_user_management.update_item(
            TableName='UserManagement',
            Key={
                'PK': {'S': pk_value},
                'SK': {'S': sk_value},
            },
            UpdateExpression='SET password = :val',
            ExpressionAttributeValues={
                ':val': {'S': new_password_hash.decode('utf-8')}
            },
            ReturnValues="UPDATED_NEW"
        )
        print(f"{pk_value} updated successfully.")
        update_data = get_user_json(get_user(pk_value[5:])) if entity_type == 'User' else get_shop_json(get_shop(pk_value[5:]))
        return update_data
    except ClientError as e:
        print(f"Error updating: {e}")
        raise e


# Function to add a user to the dynamodb
def add_user(email, password, username, address, phone):
    try:
        if user_in_db(email) is not None:
            logging.info("Test...")
            return None

        # Generate UUID for the new user
        user_uuid = str(uuid.uuid4())

        # Hash the password before storing it
        hashed_password = hash_password(password)

        # Replace None with an empty string for optional fields
        address = address if address is not None else ''
        phone = phone if phone is not None else ''

        # Put the new item into the table
        db_user_management.put_item(
            TableName='UserManagement',
            Item={
                'PK': {'S': f'USER#{user_uuid}'},
                'SK': {'S': f'PROFILE#{user_uuid}'},
                'type': {'S': 'User'},
                'profile_picture': {'S': ''},
                'email': {'S': email},
                'username': {'S': username},
                'password': {'S': hashed_password.decode('utf-8')},
                'address': {'S': address},
                'phone': {'S': phone}
            }
        )
        print("User added with UUID:", user_uuid)
        logging.info("Test...")
        return get_user_json(get_user(user_uuid))
    except ClientError as e:
        print("Error adding user:", e)


# Function to add a shop to the dynamodb
def add_shop(shop_name, email, password, address, phone, description):
    try:
        # Check if the user already exists
        if user_in_db(email) is not None:
            return None

        # Generate UUID for the new user
        shop_uuid = str(uuid.uuid4())

        # Hash the password before storing it
        hashed_password = hash_password(password)

        # Replace None with an empty string for optional fields
        address = address if address is not None else ''
        phone = phone if phone is not None else ''
        description = description if description is not None else ''

        # Put the new item into the table
        db_user_management.put_item(
            TableName='UserManagement',
            Item={
                'PK': {'S': f'SHOP#{shop_uuid}'},
                'SK': {'S': f'DETAILS#{shop_uuid}'},
                'type': {'S': 'Shop'},
                'profile_picture': {'S': ''},
                'email': {'S': email},
                'shop_name': {'S': shop_name},
                'description': {'S': description},
                'password': {'S': hashed_password.decode('utf-8')},
                'address': {'S': address},
                'phone': {'S': phone}
            }
        )
        print("Shop added with UUID:", shop_uuid)
        return get_shop_json(get_shop(shop_uuid))
    except ClientError as e:
        print("Error adding shop:", e)


def user_in_db(email):
    try:
        response = db_user_management.query(
            TableName='UserManagement',
            IndexName='EmailIndex',
            KeyConditionExpression='email = :email',
            ExpressionAttributeValues={':email': {'S': email}}
        )
        return response['Items'][0] if response['Items'] else None
    except ClientError as e:
        print(f"Error checking email existence: {e}")
        return None


def update_entity(entity_uuid, attributes):
    try:
        entity_type = get_entity_type(entity_uuid)
        if entity_type is None:
            return False
        logging.error(entity_type)
        # Base update expression setup
        update_expression = "set "
        expression_attribute_values = {}

        # Dynamically build the update expression based on provided attributes
        for key, value in attributes.items():
            update_expression += f"{key} = :{key}, "
            expression_attribute_values[f":{key}"] = {'S': value}

        # Remove the trailing comma and space from the update expression
        update_expression = update_expression.rstrip(", ")

        # Determine the key prefix based on the entity type
        pk_value, sk_value = pk_sk_values(entity_uuid)

        # Execute the update operation
        db_user_management.update_item(
            TableName='UserManagement',
            Key={
                'PK': {'S': pk_value},
                'SK': {'S': sk_value},
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        print(f"{pk_value} updated successfully.")
        update_data = get_user_json(get_user(pk_value[5:])) if entity_type == 'User' else get_shop_json(get_shop(pk_value[5:]))
        return update_data
    except ClientError as e:
        print(f"Error updating: {e}")
        raise e


def get_entity(entity_uuid):
    """
    Fetch an entity (user or shop) from the DynamoDB table using the entity UUID.

    :param entity_uuid: The UUID of the entity to fetch.
    :return: The entity item if found, None otherwise.
    """
    try:
        # Attempt to fetch the user
        user_response = get_user(entity_uuid)
        if user_response.get('Item') is not None:
            return user_response

        # If not found, attempt to fetch the shop
        shop_response = get_shop(entity_uuid)
        if shop_response.get('Item') is not None:
            return shop_response
        # If no entity is found, return None
        return None
    except ClientError as e:
        print("Error getting entity:", e)


def get_entity_json(entity_uuid):
    try:
        entity = get_entity(entity_uuid)
        if entity is None:
            return False
        entity_type = entity.get('Item')['type'].get('S')
        return get_user_json(get_user(entity_uuid)) if entity_type == 'User' else get_shop_json(get_shop(entity_uuid))
    except ClientError as e:
        print("Error getting entity:", e)


def get_entity_type(entity_uuid):
    try:
        response = get_entity(entity_uuid)
        # Check if 'Item' is in the response and it is not None
        if response is None:
            return None
        return response['Item'].get('type', {}).get('S')
    except ClientError as e:
        print("Error getting entity:", e)


# Uploads a profile picture to S3 and updates the user's DynamoDB entry.
def update_profile_picture(entity_uuid, file_path, filename):
    try:
        bucket_name = 'userview'
        s3_client.upload_file(file_path, bucket_name, f"{entity_uuid}/{filename}")
        image_url = f"http://{bucket_name}.s3.localhost.localstack.cloud:4566/{entity_uuid}/{filename}"

        response = pk_sk_values(entity_uuid)
        if not response:
            return False
        pk_value, sk_value = response

        # Update the item in the table to include the profile picture URL
        response = db_user_management.update_item(
            TableName='UserManagement',
            Key={
                'PK': {'S': pk_value},
                'SK': {'S': sk_value},
            },
            UpdateExpression='SET profile_picture = :val',
            ExpressionAttributeValues={
                ':val': {'S': image_url}
            },
            ReturnValues="UPDATED_NEW"
        )
        print(f"Profile picture updated:", response)
        return response
    except ClientError as e:
        print(f"Error updating profile picture:", e)


def delete_user(user_uuid):
    try:
        response = pk_sk_values(user_uuid)
        if response:
            pk_value, sk_value = response
            # Perform the delete operation
            db_user_management.delete_item(
                TableName='UserManagement',
                Key={
                    'PK': {'S': f'USER#{user_uuid}'},
                    'SK': {'S': f'PROFILE#{user_uuid}'}
                }
            )
            return True
        return False
    except ClientError as e:
        print(f"Error deleting: {e}")
        return False


def delete_shop(shop_uuid):
    try:
        response = pk_sk_values(shop_uuid)
        if response:
            # Perform the delete operation
            db_user_management.delete_item(
                TableName='UserManagement',
                Key={
                    'PK': {'S': f'SHOP#{shop_uuid}'},
                    'SK': {'S': f'DETAILS#{shop_uuid}'}
                }
            )
            return True
        return False
    except ClientError as e:
        print(f"Error deleting: {e}")
        return False

def pk_sk_values(entity_uuid):
    try:
        entity_type = get_entity_type(entity_uuid)
        if entity_type is None:
            return False
        pk_prefix = 'USER' if entity_type == 'User' else 'SHOP'
        sk_prefix = 'PROFILE' if entity_type == 'User' else 'DETAILS'
        pk_value = f'{pk_prefix}#{entity_uuid}'
        sk_value = f'{sk_prefix}#{entity_uuid}'
        return pk_value, sk_value
    except ClientError as e:
        print(f"Error updating: {e}")
        raise e


def get_user(user_uuid):
    try:
        response = db_user_management.get_item(
            TableName='UserManagement',
            Key={
                'PK': {'S': f'USER#{user_uuid}'},
                'SK': {'S': f'PROFILE#{user_uuid}'}
            }
        )
        return response
    except ClientError as e:
        print("Error getting user:", e)


# Function to get a user by UUID
def get_user_json(user):
    try:
        user_dict = {
            'user_id': user.get('Item', {}).get('PK', {}).get('S', None)[5:]
                if user.get('Item', {}).get('PK', {}).get('S', None) else None,
            'type': user.get('Item', {}).get('type', {}).get('S', None),
            'profile_picture': user.get('Item', {}).get('profile_picture', {}).get('S', None),
            'email': user.get('Item', {}).get('email', {}).get('S', None),
            'username': user.get('Item', {}).get('username', {}).get('S', None),
            'address': user.get('Item', {}).get('address', {}).get('S', None),
            'phone': user.get('Item', {}).get('phone', {}).get('S', None)
        }
        return user_dict
    except ClientError as e:
        print("Error getting user:", e)


# Function to get a user by UUID
def get_shop(shop_uuid):
    try:
        response = db_user_management.get_item(
            TableName='UserManagement',
            Key={
                'PK': {'S': f'SHOP#{shop_uuid}'},
                'SK': {'S': f'DETAILS#{shop_uuid}'}
            }
        )
        return response
    except ClientError as e:
        print("Error getting shop:", e)


# Function to get a user by UUID
def get_shop_json(shop):
    try:
        shop_dict = {
            'shop_id': shop.get('Item', {}).get('PK', {}).get('S', None)[5:]
                if shop.get('Item', {}).get('PK', {}).get('S', None) else None,
            'type': shop.get('Item', {}).get('type', {}).get('S', None),
            'profile_picture': shop.get('Item', {}).get('profile_picture', {}).get('S', None),
            'email': shop.get('Item', {}).get('email', {}).get('S', None),
            'shop_name': shop.get('Item', {}).get('shop_name', {}).get('S', None),
            'description': shop.get('Item', {}).get('description', {}).get('S', None),
            'address': shop.get('Item', {}).get('address', {}).get('S', None),
            'phone': shop.get('Item', {}).get('phone', {}).get('S', None)
        }
        return shop_dict
    except ClientError as e:
        print("Error getting user:", e)