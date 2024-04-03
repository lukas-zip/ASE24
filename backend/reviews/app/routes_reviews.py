from flask import Flask, jsonify, request
from flask_cors import CORS
import boto3
from app import app, dynamodb_reviews
import uuid
from botocore.exceptions import ClientError

# Test if endpoint is available
@app.route('/review', methods=['GET'])
def test():
    # Return success response
    return jsonify({'message': 'Test successful'}), 201

# Adding review by retrieving data from post request and saving into dynamodb
@app.route('/review/add', methods=['POST'])
def route_add_review():
    data = request.json
    product_id = data.get('product_id')
    customer_id = data.get('customer_id')
    reviewcontent = data.get('reviewcontent')
    rating = data.get('rating')
    time_lastedit = data.get('time_lastedit')
    time_created = data.get('time_created')

    if not product_id or not customer_id or not rating:
        return jsonify({'message': 'Product_ID, Customer_ID and rating are required!', "status": False}), 400

    try:
        message, status = dynamodb_reviews.add_review(product_id,customer_id,reviewcontent,rating,time_lastedit,time_created)
        if status == True:
            return jsonify({'value': message,'status': status}), 200
        else:
            return jsonify({'message': message,'status': status}), 200
    except ClientError as e:
        print("Error adding review:", e)

# Delete review 
@app.route('/review/delete', methods=['DELETE'])
def route_delete_review():
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
@app.route('/review/check', methods=['GET'])
def route_check_review():
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

# edit existing review
@app.route('/review/edit', methods=['PUT'])
def route_edit_review():
    data = request.json
    review_id = data.get('review_id')
    product_id = data.get('product_id')
    user_id = data.get('customer_id')
    reviewcontent = data.get('reviewcontent')
    rating = data.get('rating')
    time_lastedit = data.get('time_lastedit')
    time_created = data.get('time_created')

    #if not product_id or not review_id or not customer_id:
    #    return jsonify({'error': 'Product_ID,customer_id and review_ID are required!'}), 400
    try:
        item, status = dynamodb_reviews.edit_review(review_id,product_id, user_id,reviewcontent,rating,time_lastedit,time_created)
        if status == True:
            return jsonify({'value': item,'status': status}), 200
        else:
            return jsonify({'message': item,'status': status}), 200
    except ClientError as e:
        print("Error updating review:", e)
        return jsonify({'error': 'Failed to update review'}), 500
    
@app.route('/review/get', methods=['GET'])
def route_get_review():
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
    
@app.route('/review/getbatch',methods=['GET'])
def route_get_batch():
    data = request.json
    product_id = data.get('product_id')

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