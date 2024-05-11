from flask import Flask, jsonify, request
from flask_cors import CORS
import boto3
from app import dynamodb_reviews
import uuid
from botocore.exceptions import ClientError
from flask import Blueprint

route_blueprint = Blueprint('', __name__,)

# Test if endpoint is available
@route_blueprint.route('/', methods=['GET'])
def test():
    try:
        return jsonify({'status': True, 'value': 'Test successful'}), 200
    except ClientError as e:
        print("Error adding review:", e)

# Adding review by retrieving data from post request and saving into dynamodb
@route_blueprint.route('/review', methods=['POST'])
def route_add_review():
    """
    Adds a new review for a product.

    :param data: A dictionary containing the review details including product_id, customer_id, reviewcontent, and rating.
    :return: A JSON response indicating the success or failure of the review addition.
    :raises ClientError: If an error occurs while adding the review to DynamoDB.
    """
    data = request.json
    product_id = data.get('product_id')
    customer_id = data.get('customer_id')
    reviewcontent = data.get('reviewcontent')
    rating = data.get('rating')

    if not product_id or not customer_id or not rating:
        return jsonify({'message': 'Product_ID, Customer_ID and rating are required!', "status": False}), 400

    try:
        message, status = dynamodb_reviews.add_review(product_id,customer_id,reviewcontent,rating)
        if status == True:
            return jsonify({'value': message,'status': status}), 200
        else:
            return jsonify({'message': message,'status': status}), 200
    except ClientError as e:
        print("Error adding review:", e)

# Delete review 
@route_blueprint.route('/review', methods=['DELETE'])
def route_delete_review():
    """
    Deletes a review for a product.

    :param data: A dictionary containing the review details including review_id, product_id, and customer_id.
    :return: A JSON response indicating the success or failure of the review deletion.
    :raises ClientError: If an error occurs while deleting the review from DynamoDB.
    """
    data = request.json
    review_id = data.get('review_id')
    product_id = data.get('product_id')
    customer_id = data.get('customer_id')

    if not product_id or not review_id or not customer_id:
        return jsonify({'error': 'Product_ID,customer_id and review_ID are required!'}), 400
    try:
        message, status = dynamodb_reviews.delete_review(review_id,product_id,customer_id)
        if status == True:
            return jsonify({'value': message,'status': status}), 200
        else:
            return jsonify({'message': message,'status': status}), 200
    except ClientError as e:
        print("Error deleting review:", e)
        return jsonify({'error': 'Failed to delete review'}), 500

# Check if review already exists
@route_blueprint.route('/review/check', methods=['GET'])
def route_check_review():
    """
    Checks if a review exists for a product by a customer.

    :param data: A dictionary containing the review details including product_id and customer_id.
    :return: A JSON response indicating the existence of the review.
    :raises ClientError: If an error occurs while checking the review in DynamoDB.
    """
    data = request.json
    product_id = data.get('product_id')
    customer_id = data.get('customer_id')

    if not product_id or not customer_id:
        return jsonify({'error': 'Product_ID and Customer_ID are required!'}), 400
    try:
        message, status = dynamodb_reviews.check_review(customer_id,product_id)
        if status == True:
            return jsonify({'value': message,'status': status}), 200
        else:
            return jsonify({'message': message,'status': status}), 200
    except ClientError as e:
        print("Error checking review:", e)
        return jsonify({'error': 'Failed to check review'}), 500

# Edit existing review
@route_blueprint.route('/review', methods=['PUT'])
def route_edit_review():
    """
    Edits an existing review for a product.

    :param data: A dictionary containing the review details including review_id, product_id, customer_id, reviewcontent, and rating.
    :return: A JSON response indicating the success or failure of the review editing.
    :raises ClientError: If an error occurs while editing the review in DynamoDB.
    """
    data = request.json
    review_id = data.get('review_id')
    product_id = data.get('product_id')
    user_id = data.get('customer_id')
    reviewcontent = data.get('reviewcontent')
    rating = data.get('rating')

    try:
        item, status = dynamodb_reviews.edit_review(review_id,product_id, user_id,reviewcontent,rating)
        if status == True:
            return jsonify({'value': item,'status': status}), 200
        else:
            return jsonify({'message': item,'status': status}), 200
    except ClientError as e:
        print("Error updating review:", e)
        return jsonify({'error': 'Failed to update review'}), 500
    
# Return single review
@route_blueprint.route('/review/getsingle', methods=['GET'])
def route_get_review():
    """
    Retrieves a single review for a product.

    :param data: A dictionary containing the review details including review_id and product_id.
    :return: A JSON response containing the review details.
    :raises ClientError: If an error occurs while retrieving the review from DynamoDB.
    """
    data = request.json
    review_id = data.get('review_id')
    product_id = data.get('product_id')

    if not review_id or not product_id:
        return jsonify({'message': 'ID is required!'}), 400
    try:
        item, status = dynamodb_reviews.get_review(review_id,product_id)
        if status == True:
            return jsonify({'value': item,'status': status}), 200
        else:
            return jsonify({'message': item,'status': status}), 200
    except ClientError as e:
        print("Error adding review:", e)
        return jsonify({'error': 'Failed to get review'}), 500
    
# Return all reviews for a product
@route_blueprint.route('/review/<product_id>',methods=['GET'])
def route_get_batch(product_id):
    """
    Retrieves all reviews for a specific product.

    :param product_id: The ID of the product.
    :return: A JSON response containing the reviews for the product.
    :raises ClientError: If an error occurs while retrieving the reviews from DynamoDB.
    """

    if not product_id:
        return jsonify({'error': 'ID is required!'}), 400
    try:
        items, status = dynamodb_reviews.get_batch(product_id)
        if status == True:
            return jsonify({'value': items,'status': status}), 200
        else:
            return jsonify({'message': items,'status': status}), 200
    except ClientError as e:
        print("Error adding review:", e)
        return jsonify({'error': 'Failed to get review'}), 500