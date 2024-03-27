from flask import Flask, jsonify, request
from ASE24.backend.reviews.app import dummydata_reviews
from app import dynamodb_reviews
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    dynamodb_reviews.create_review_tables()
    dummydata_reviews.add_dummy_data()
    CORS(app)
    return app

app = create_app()