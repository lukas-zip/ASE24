from flask import request
from flask import Blueprint
from app import app, db
from app.models import User

user_api_blueprint = Blueprint('user_api', __name__)

@app.route('/')
def index():
    return 'This is the index page'

@user_api_blueprint.route('/')
def index():
    return "Testing"

@user_api_blueprint.route('/users', methods=['GET'])
def get_users():
    return {"msg": "Return users"}

@user_api_blueprint.route('/user/register', methods=['POST'])
def register_user():
    example_data = request.get_json()
    value = example_data['key']
    return {"msg": f"Register user with input: {value}"}