import boto3
import uuid
from botocore.exceptions import ClientError
import bcrypt
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def get_dynamodb_resource():
    """
    Initializes and returns a connection to the DynamoDB and S3 services using predefined settings for LocalStack.

    :return: A tuple containing the DynamoDB and S3 client objects.
    """
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
    """
    Creates an S3 bucket named 'userview' on LocalStack. Logs the result of the operation.

    :raises ClientError: If there's an error during the bucket creation process.
    """
    try:
        bucket_name = 'userview'
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} created successfully.")
    except ClientError as e:
        print(f"Error creating bucket: {e}")


# Function to create the profiles table
def create_user_management_tables(dynamodb=db_user_management):
    """
    Creates a table named 'UserManagement' in DynamoDB on LocalStack with the necessary schema and indexes for user management.

    :param dynamodb: DynamoDB client instance (default is db_user_management).
    :return: The response from the create_table operation containing metadata about the created table.
    :raises ClientError: If the table creation fails.
    """
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
    """
    Deletes the 'UserManagement' table from DynamoDB on LocalStack. Logs if the table does not exist.

    :raises ResourceNotFoundException: If the table does not exist.
    """
    try:
        db_user_management.delete_table(TableName='UserManagement')
    except db_user_management.exceptions.ResourceNotFoundException:
        print("Table does not exist.")

def hash_password(password):
    """
    Hashes a password using bcrypt.

    :param password: The password to hash.
    :return: The hashed password as a bytes object.
    """
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
    """
    Attempts to change the password for a given entity (user or shop) after verifying the old password.

    :param entity_uuid: The UUID of the entity whose password is to be changed.
    :param old_password: The current password for verification.
    :param new_password: The new password to set if the old password is correctly verified.
    :return: On success, returns update data for the entity; on failure, returns a mismatch message or raises a ClientError.
    """
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
def add_user(email, password, username, address, phone, profile_picture, dummyid=None):
    """
    Adds a new user to the DynamoDB 'UserManagement' table with provided details.

    :param email: User's email address.
    :param password: User's password (will be hashed before storage).
    :param username: User's username.
    :param address: User's address (optional).
    :param phone: User's phone number (optional).
    :param profile_picture: URL to the user's profile picture (optional).
    :param dummyid: Optional UUID to use instead of generating a new one.
    :return: JSON dictionary containing user data if successful, None if user exists.
    :raises ClientError: If there is an error during the user addition process.
    """
    try:
        if user_in_db(email) is not None:
            return None

        # Generate UUID for the new user
        if dummyid is None:
            user_uuid = str(uuid.uuid4())
        else:
            user_uuid = dummyid

        # Hash the password before storing it
        hashed_password = hash_password(password)

        # Replace None with an empty string for optional fields
        address = address if address is not None else ''
        phone = phone if phone is not None else ''
        profile_picture = profile_picture if profile_picture is not None else ''

        # Put the new item into the table
        db_user_management.put_item(
            TableName='UserManagement',
            Item={
                'PK': {'S': f'USER#{user_uuid}'},
                'SK': {'S': f'PROFILE#{user_uuid}'},
                'type': {'S': 'User'},
                'profile_picture': {'S': profile_picture},
                'email': {'S': email},
                'username': {'S': username},
                'password': {'S': hashed_password.decode('utf-8')},
                'address': {'S': address},
                'phone': {'S': phone}
            }
        )
        print("User added with UUID:", user_uuid)
        return get_user_json(get_user(user_uuid))
    except ClientError as e:
        print("Error adding user:", e)


# Function to add a shop to the dynamodb
def add_shop(shop_name, email, password, address, phone, description, profile_picture, shop_pictures, dummyid=None):
    """
    Adds a new shop to the DynamoDB 'UserManagement' table with provided details.

    :param shop_name: Name of the shop.
    :param email: Shop owner's email address.
    :param password: Shop owner's password (will be hashed before storage).
    :param address: Shop's address (optional).
    :param phone: Shop's phone number (optional).
    :param description: Description of the shop (optional).
    :param profile_picture: URL to the shop's profile picture (optional).
    :param shop_pictures: List of URLs to pictures of the shop (optional).
    :param dummyid: Optional UUID to use instead of generating a new one.
    :return: JSON dictionary containing shop data if successful, None if shop exists.
    :raises ClientError: If there is an error during the shop addition process.
    """
    try:
        # Check if the user already exists
        if user_in_db(email) is not None:
            return None

        # Generate UUID for the new user
        if dummyid is None:
            shop_uuid = str(uuid.uuid4())
        else:
            shop_uuid = dummyid

        # Hash the password before storing it
        hashed_password = hash_password(password)

        # Replace None with an empty string for optional fields
        address = address if address is not None else ''
        phone = phone if phone is not None else ''
        description = description if description is not None else ''
        profile_picture = profile_picture if profile_picture is not None else ''
        shop_pictures = shop_pictures if shop_pictures is not None else ['']
        # Put the new item into the table
        db_user_management.put_item(
            TableName='UserManagement',
            Item={
                'PK': {'S': f'SHOP#{shop_uuid}'},
                'SK': {'S': f'DETAILS#{shop_uuid}'},
                'type': {'S': 'Shop'},
                'profile_picture': {'S': profile_picture},
                'shop_pictures': {'SS': shop_pictures},
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
    """
    Checks if a user or shop exists in the DynamoDB 'UserManagement' table based on their email.

    :param email: Email address to search for in the database.
    :return: The first item found matching the email or None if no match is found.
    :raises ClientError: If there is an error querying the database.
    """
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
    """
    Updates attributes of an existing entity (user or shop) in the DynamoDB 'UserManagement' table.

    :param entity_uuid: UUID of the entity to update.
    :param attributes: Dictionary of attribute names and their new values to update.
    :return: Update data for the entity if successful, or raises a
    """
    try:
        entity_type = get_entity_type(entity_uuid)
        if entity_type is None:
            return False
        # Base update expression setup
        update_expression = "set "
        expression_attribute_values = {}

        # Dynamically build the update expression based on provided attributes
        for key, value in attributes.items():
            update_expression += f"{key} = :{key}, "
            if key in ['shop_pictures']:
                expression_attribute_values[f":{key}"] = {'SS': value}
            else:
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
    """
    Fetches a JSON representation of an entity (either a user or a shop) from DynamoDB based on its UUID.

    :param entity_uuid: The UUID of the entity to fetch.
    :return: A dictionary representation of the entity if found, otherwise False if the entity does not exist.
    :raises ClientError: If an error occurs while fetching the entity data.
    """
    try:
        entity = get_entity(entity_uuid)
        if entity is None:
            return False
        entity_type = entity.get('Item')['type'].get('S')
        return get_user_json(get_user(entity_uuid)) if entity_type == 'User' else get_shop_json(get_shop(entity_uuid))
    except ClientError as e:
        print("Error getting entity:", e)


def get_entity_type(entity_uuid):
    """
    Determines the type of an entity (user or shop) based on its UUID.

    :param entity_uuid: The UUID of the entity.
    :return: A string representing the type of the entity ('User' or 'Shop') if found, None otherwise.
    :raises ClientError: If an error occurs during the fetch operation.
    """
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
    """
    Uploads a profile picture to an S3 bucket and updates the corresponding DynamoDB entry to include the new image URL.

    :param entity_uuid: The UUID of the entity (user or shop).
    :param file_path: The local path to the file to be uploaded.
    :param filename: The filename under which the file should be stored in the bucket.
    :return: The update response from DynamoDB if successful, otherwise False if the keys are invalid.
    :raises ClientError: If an error occurs during the file upload or the DynamoDB update.
    """
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
    """
    Deletes a user from the DynamoDB table based on their UUID.

    :param user_uuid: The UUID of the user to delete.
    :return: True if the user was successfully deleted, False otherwise.
    :raises ClientError: If an error occurs during the deletion process.
    """
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
    """
    Deletes a shop from the DynamoDB table based on its UUID.

    :param shop_uuid: The UUID of the shop to delete.
    :return: True if the shop was successfully deleted, False otherwise.
    :raises ClientError: If an error occurs during the deletion process.
    """
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
    """
    Generates primary key (PK) and sort key (SK) values for an entity in DynamoDB based on its UUID.

    :param entity_uuid: The UUID of the entity.
    :return: A tuple containing the PK and SK values, or False if the entity type is unknown.
    :raises ClientError: If an error occurs determining the entity type.
    """
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
    """
    Retrieves a user from the DynamoDB table based on their UUID.

    :param user_uuid: The UUID of the user.
    :return: The user's data as fetched from DynamoDB, or logs an error if not found.
    :raises ClientError: If an error occurs during the fetch operation.
    """
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
    """
    Converts DynamoDB user item data into a JSON-friendly dictionary format.

    :param user: The DynamoDB user item.
    :return: A dictionary containing the user's details.
    :raises ClientError: If an error occurs while retrieving the user data.
    """
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
    """
    Retrieves a shop from the DynamoDB table based on its UUID.

    :param shop_uuid: The UUID of the shop.
    :return: The shop's data as fetched from DynamoDB, or logs an error if not found.
    :raises ClientError: If an error occurs during the fetch operation.
    """
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
    """
    Converts DynamoDB shop item data into a JSON-friendly dictionary format.

    :param shop: The DynamoDB shop item.
    :return: A dictionary containing the shop's details.
    :raises ClientError: If an error occurs while retrieving the shop data.
    """
    try:
        pictures = shop.get('Item', {}).get('shop_pictures', {}).get('SS', None)
        if pictures == ['']:
            shop_pictures = []
        else:
            shop_pictures = pictures
        shop_dict = {
            'shop_id': shop.get('Item', {}).get('PK', {}).get('S', None)[5:]
                if shop.get('Item', {}).get('PK', {}).get('S', None) else None,
            'type': shop.get('Item', {}).get('type', {}).get('S', None),
            'profile_picture': shop.get('Item', {}).get('profile_picture', {}).get('S', None),
            'shop_pictures': shop_pictures,
            'email': shop.get('Item', {}).get('email', {}).get('S', None),
            'shop_name': shop.get('Item', {}).get('shop_name', {}).get('S', None),
            'description': shop.get('Item', {}).get('description', {}).get('S', None),
            'address': shop.get('Item', {}).get('address', {}).get('S', None),
            'phone': shop.get('Item', {}).get('phone', {}).get('S', None)
        }
        return shop_dict
    except ClientError as e:
        print("Error getting user:", e)