from flask import request
from flask import Blueprint
from app import app, db
from app.models import Product

product_catalogue_api_blueprint = Blueprint('product_api', __name__)

@product_catalogue_api_blueprint.route('/', methods=['GET'])
def index():
    return {"msg": "Test product"}

@product_catalogue_api_blueprint.route('/products', methods=['GET'])
def get_products():
    return {"msg": "Return products"}

@product_catalogue_api_blueprint.route('/product/new', methods=['POST'])
def post_products():
    example_data = request.get_json()
    value = example_data['key']
    return {"msg": f"Post products: {value}"}
