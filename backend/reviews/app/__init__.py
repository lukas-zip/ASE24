from flask import Flask, jsonify, request
#from ASE24.backend.reviews.app import dummydata_reviews
from app import dynamodb_reviews
from app import routes_reviews
from flask_cors import CORS
from app.routes_reviews import route_blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(route_blueprint)
    CORS(app)
    return app

app = create_app()

with app.app_context():
    dynamodb_reviews.create_review_tables()
    #dummydata_reviews.add_dummy_data()