#from flask import Flask, jsonify, request
#from flask_cors import CORS
#from app.routes import route_blueprint
from app import dynamodb, s3, dummydata_products
from flask import Flask
from flask_cors import CORS
from app.routes import route_blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(route_blueprint)
    CORS(app)
    return app

app = create_app()

with app.app_context():
    dynamodb.create_product_table()
    dynamodb.create_product_owner_index()
    s3.create_bucket()
    dynamodb.create_gsi()
    dummydata_products.add_dummy_data()