from flask import jsonify, request
from app import dynamodb
from werkzeug.utils import secure_filename
import os
import re
from app import s3
from botocore.exceptions import ClientError
from io import BytesIO
from urllib.parse import quote_plus
from flask import Blueprint


route_blueprint = Blueprint('', __name__,)

# Test if endpoint is available
@route_blueprint.route('/', methods=['GET'])
def test():
    """
    A simple test route that returns a success message and status. This function is a placeholder to confirm the API endpoint is reachable.

    :return: A JSON response with a success status and message.
    """
    print("Hello, world!")
    return jsonify({'status': True, 'value': 'Test successful'}), 200


@route_blueprint.route('/<entity>', methods=['POST'])
def register_entity(entity):
    """
    Registers an entity, which can be either a 'user' or 'shop'. The function dynamically calls the appropriate registration function based on the entity type.

    :param entity: A string specifying the entity type ('users' or 'shops').
    :return: A JSON response indicating the result of the registration attempt.
    :raises ClientError: If there is an issue with DynamoDB operations.
    """
    try:
        data = request.json
        if entity == 'users':
            return register_user(data)
        elif entity == 'shops':
            return register_shop(data)
        else:
            return jsonify({'status': False, 'message': 'Invalid action'}), 400
    except ClientError as e:
        print(f"Error: {e}")
        return jsonify({'status': False, 'message': f'An error occurred'}), 500


# User registration by retrieving data from post request and saving into dynamodb
def register_user(data):
    """
    Registers a new user with the provided details, saving the data to DynamoDB.

    :param data: A dictionary containing user details.
    :return: A JSON response indicating the success or failure of the registration.
    :raises ClientError: If an error occurs while adding the user to DynamoDB.
    """
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    address = data.get('address')
    phone = data.get('phone')
    profile_picture = data.get('profile_picture')

    if not email or not password or not username:
        return jsonify({'status': False, 'message': 'Email, username and password are required!'}), 400
    # Check if the email is in the right format
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return jsonify({'status': False, 'message': 'Invalid email format!'}), 400

    try:
        new_user = dynamodb.add_user(email, password, username, address, phone, profile_picture)
        if new_user is None:
            return jsonify({'status': False, 'message': 'Unable to register the user. E-Mail address may already be in use.'}), 400
        return jsonify({'status': True, 'value': new_user}), 200

    except ClientError as e:
        print("Error adding user:", e)
        return jsonify({'status': False, 'message': 'An error occurred while registering the user'}), 500

# Shop registration by retrieving data from post request and saving into dynamodb
def register_shop(data):
    """
    Registers a new shop with the provided details, saving the data to DynamoDB.

    :param data: A dictionary containing shop details.
    :return: A JSON response indicating the success or failure of the registration.
    :raises ClientError: If an error occurs while adding the shop to DynamoDB.
    """
    email = data.get('email')
    shop_name = data.get('shop_name')
    description = data.get('description')
    password = data.get('password')
    address = data.get('address')
    phone = data.get('phone')
    profile_picture = data.get('profile_picture')
    shop_pictures = data.get('shop_pictures')

    if not email or not shop_name or not password:
        return jsonify({'status': False, 'message': 'Email, shop name, address and password are required!'}), 400
    # Check if the email is in the right format
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return jsonify({'status': False, 'message': 'Invalid email format!'}), 400

    try:
        new_shop = dynamodb.add_shop(shop_name, email, password, address, phone, description, profile_picture, shop_pictures)
        if new_shop is None:
            return jsonify({'status': False, 'message': 'Unable to register the shop. E-Mail address may already be in use.'}), 400
        return jsonify({'status': True, 'value': new_shop}), 200

    except ClientError as e:
        print("Error adding user:", e)
        return jsonify({'status': False, 'message': 'An error occurred while registering the shop'}), 500


# Check if user already  exists and provide login to platform
@route_blueprint.route('/login', methods=['POST'])
def login():
    """
    Handles user login by checking provided credentials against the database entries.

    :return: A JSON response indicating success if credentials are valid, or an error message otherwise.
    :raises ClientError: If a DynamoDB operation error occurs.
    """
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'status': False, 'message': 'Email and password are required'}), 400

    try:
        # Check if entity exists and password is correct
        login = dynamodb.check_login(email, password)
        if login:
            return jsonify({'status': True, 'value': login}), 200
        else:
            return jsonify({'status': False, 'message': 'Invalid login credentials'}), 401
    except ClientError as e:
        return jsonify({'status': False, 'message': str(e)}), 500


@route_blueprint.route('/<entity>/<entity_uuid>', methods=['PUT'])
def update_entity(entity, entity_uuid):
    """
    Updates an entity (user or shop) based on the provided JSON data and action type specified within the data.

    :param entity: The type of the entity ('users' or 'shops').
    :param entity_uuid: UUID of the entity to be updated.
    :return: A JSON response indicating the result of the update attempt.
    :raises ClientError: If an error occurs while updating the entity in DynamoDB.
    """
    try:
        data = request.json
        action = data.get('action')
        if entity == 'users' and action == 'update':
            return update_user(data, entity_uuid)
        elif entity == 'shops' and action == 'update':
            return update_shop(data, entity_uuid)
        elif action == 'password':
            return change_password(data, entity_uuid)
        else:
            jsonify({'status': False, 'message': 'Invalid action'}), 400
    except ClientError as e:
        print(f"Error deleting {entity_uuid}: {e}")
        return jsonify({'status': False, 'message': f'An error occurred'}), 500


# Update function for shop
def update_shop(data, entity_uuid):
    """
    Updates the shop details in DynamoDB based on provided data.

    :param data: A dictionary containing the new shop details.
    :param entity_uuid: UUID of the shop to be updated.
    :return: A JSON response indicating success or failure of the update.
    :raises ClientError: If an error occurs during the DynamoDB update operation.
    """
    shop_name = data.get('shop_name')
    description = data.get('description')
    email = data.get('email')
    address = data.get('address')
    phone = data.get('phone')
    profile_picture = data.get('profile_picture')
    shop_pictures = data.get('shop_pictures')

    if not email or not shop_name:
        return jsonify({'status': False, 'message': 'Email and shop name cannot be empty!'}), 400

    # Check if the email is in the right format
    if email:
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return jsonify({'status': False, 'message': 'Invalid email format!'}), 400

    if shop_pictures == []:
        shop_pictures = [""]

    attributes = {
        'email': email,
        'shop_name': shop_name,
        'description': description,
        'address': address,
        'phone': phone,
        'profile_picture': profile_picture,
        'shop_pictures': shop_pictures
    }

    try:
        update_response = dynamodb.update_entity(entity_uuid, attributes)
        if update_response:
            return jsonify({'status': True, 'value': update_response}), 200
        else:
            return jsonify({'status': False, 'message': 'Failed to update shop'}), 400
    except ClientError as e:
        print(f"Error updating shop: {e}")
        return jsonify({'status': False, 'message': 'An error occurred while updating the shop'}), 500


def update_user(data, entity_uuid):
    """
    Updates user details in DynamoDB based on provided data.

    :param data: A dictionary containing the new user details.
    :param entity_uuid: UUID of the user to be updated.
    :return: A JSON response indicating success or failure of the update.
    :raises ClientError: If an error occurs during the DynamoDB update operation.
    """
    # Retrieve the data sent in the request
    email = data.get('email')
    username = data.get('username')
    address = data.get('address')
    phone = data.get('phone')
    profile_picture = data.get('profile_picture')

    if not email or not username:
        return jsonify({'status': False, 'message': 'Email and username cannot be empty!'}), 400

    # Check if the email is in the right format
    if email:
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return jsonify({'status': False, 'message': 'Invalid email format!'}), 400

    attributes = {
        'email': email,
        'username': username,
        'address': address,
        'phone': phone,
        'profile_picture': profile_picture
    }

    try:
        update_response = dynamodb.update_entity(entity_uuid, attributes)
        if update_response:
            return jsonify({'status': True, 'value': update_response}), 200
        else:
            return jsonify({'status': False, 'message': 'Failed to update user'}), 400
    except ClientError as e:
        print(f"Error updating user: {e}")
        return jsonify({'status': False, 'message': 'An error occurred while updating the user'}), 500


def change_password(data, entity_uuid):
    """
    Changes the password for a user or shop entity after verifying the old password.

    :param data: A dictionary containing the old and new passwords.
    :param entity_uuid: UUID of the entity for which the password is to be changed.
    :return: A JSON response indicating the result of the change password attempt.
    :raises ClientError: If an error occurs during the password change process in DynamoDB.
    """
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not old_password or not new_password:
        return jsonify({'status': False, 'error': 'Missing old or new password'}), 400

    try:
        response = dynamodb.change_password(entity_uuid, old_password, new_password)
        if response == "mismatch":
            return jsonify({'status': False, 'message': 'The old password is incorrect.'}), 401
        elif response:
            return jsonify({'status': True, 'value': response}), 401
        else:
            return jsonify({'status': False, 'message': 'An error occurred while changing the password. Please try again!'}), 401
    except ClientError as e:
        return jsonify({'status': False, 'message': str(e)}), 500


def update_picture(file, entity_uuid):
    """
    Handles uploading and updating a profile picture for an entity.

    :param file: File object containing the image to be uploaded.
    :param entity_uuid: UUID of the entity to which the picture belongs.
    :return: A JSON response with the outcome of the upload and update operation.
    """
    if file.filename == '':
        return jsonify({'status': False, 'message': 'No selected file'}), 400

    allowed = {'png', 'jpg', 'jpeg'}
    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed):
        return jsonify({'status': False, 'message': 'File format not supported'}), 400

    if file:
        # Secure the filename and prepend "profile" to it
        filename = secure_filename(file.filename)
        _, extension = os.path.splitext(filename)
        new_filename = f"profile_picture{extension}"
        # Set up the upload folder
        upload_folder = './profilepictures'
        os.makedirs(upload_folder, exist_ok=True)
        # Construct the full file path
        file_path = os.path.join(upload_folder, new_filename)
        # Save the file locally
        file.save(file_path)
        profile_picture_url = dynamodb.update_profile_picture(entity_uuid, file_path, new_filename)
        os.remove(file_path)

        jsonify({'status': True, 'value': 'File uploaded successfully', 'url': profile_picture_url}), 200

        response = dynamodb.get_entity_json(entity_uuid)
        if not response:
            return jsonify({'status': False, 'message': 'No entity or failed to retrieve it'}), 400
        return jsonify({'status': True, 'value': response}), 201
    return jsonify({'status': False, 'message': 'File uploaded unsuccessfull'}), 401


@route_blueprint.route('/<entity>/<entity_uuid>', methods=['GET'])
def get_entity(entity, entity_uuid):
    """
    Retrieves details for a specified entity (user or shop) based on its UUID.

    :param entity: Type of entity ('users' or 'shops').
    :param entity_uuid: UUID of the entity to retrieve.
    :return: A JSON response with the entity details if successful, or an error message otherwise.
    :raises Exception: General exceptions caught during the retrieval process.
    """
    try:
        if entity == 'users':
            response = dynamodb.get_user_json(dynamodb.get_user(entity_uuid))
        elif entity == 'shops':
            response = dynamodb.get_shop_json(dynamodb.get_shop(entity_uuid))
        else:
            return jsonify({'status': False, 'message': 'Invalid entity'}), 400

        if not response:
            return jsonify({'status': False, 'message': 'No entity or failed to retrieve it'}), 400
        return jsonify({'status': True, 'value': response}), 201
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({'status': False, 'message': 'An error occurred while fetching the entity.'}), 500


@route_blueprint.route('/<entity>/<entity_uuid>', methods=['DELETE'])
def delete_entity(entity, entity_uuid):
    """
    Deletes an entity (user or shop) from the system including associated S3 resources.

    :param entity: Type of the entity ('users' or 'shops').
    :param entity_uuid: UUID of the entity to delete.
    :return: A JSON response indicating the result of the deletion process.
    :raises ClientError: If a DynamoDB operation error occurs.
    """
    try:
        data = dynamodb.get_entity_json(entity_uuid)
        if entity == 'users':
            delete_s3_pictures(data, entity)
            response = dynamodb.delete_user(entity_uuid)
        elif entity == 'shops':
            delete_s3_pictures(data, entity)
            response = dynamodb.delete_shop(entity_uuid)
        else:
            return jsonify({'status': False, 'message': 'Invalid entity'}), 400

        if response:
            return jsonify({'status': True, 'value': f'Deleted successfully'}), 200
        else:
            return jsonify({'status': False, 'message': f'No entity or failed to delete'}), 400
    except ClientError as e:
        print(f"Error deleting {entity_uuid}: {e}")
        return jsonify({'status': False, 'message': f'An error occurred while deleting the {entity_uuid}'}), 500

def delete_s3_pictures(data, entity):
    """
    Deletes pictures associated with an entity from S3.

    :param data: A dictionary containing the entity details, including pictures.
    :param entity: Type of entity ('users' or 'shops') for context on what pictures to delete.
    """
    if entity == 'shops':
        for picture_path in data.get('shop_pictures', []):
            s3_object_key = picture_path.split('/')[-1]  # Extract object key from the picture path
            s3.delete_object(s3_object_key)
    picture_path = data.get('profile_picture', '')
    if picture_path:
        s3_object_key_profile = picture_path.split('/')[-1]  # Extract object key from the picture path
        s3.delete_object(s3_object_key_profile)

@route_blueprint.route('/picture/<action>', methods = ['POST'])
def upload_picture(action):
    """
    Uploads an image to a specified S3 bucket based on the action type ('profile' or 'shop'). Handles image uploading by validating the presence and format of the file, and then storing it in AWS S3.

    :param action: Specifies the target bucket ('profile' for user profile pictures, 'shop' for shop-related pictures).
    :return: A JSON response indicating the success or failure of the upload. Returns the URL of the uploaded image if successful.
    :raises ClientError: If there's an error during the S3 upload process.
    """
    #allowed_types = ['.jpg', '.png', '.mp4']
    if action == 'profile':
        bucket_name = 'profilepictures'
    elif action == 'shop':
        bucket_name = 'shoppictures'

    # Check if the request contains form data
    if 'image' not in request.files:
        return 'No image file provided', 400

    # Get the image file
    image_file = request.files['image']

    # Check if the image filename is empty
    if image_file.filename == '':
        return 'No selected file', 400

    object_key = image_file.filename

    #Convert bytes object to file-like object
    image_stream = BytesIO(image_file.read())

    #Construct the URL/path to the uploaded image
    s3_base_url = f'http://localhost:4566/{bucket_name}/' # Der Link ist derzeit auf Local angepasst
    image_url = s3_base_url + quote_plus(object_key)

    try:
        # Upload the image file to S3
        s3response = s3.upload_fileobj(image_stream, bucket_name, object_key)
        if s3response:
            return jsonify({'value': image_url, 'status': True}), 200
        else:
            return jsonify({'value': 'The image could unfortunately not be inserted', 'status': False}), 500
    except ClientError as e:
        print("Error uploading product picture to S3:", e)
        return