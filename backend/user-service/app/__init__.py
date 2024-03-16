from flask import Flask, jsonify, request
from app import dynamodb

def create_app():
    app = Flask(__name__)
    dynamodb.create_profiles_table()
    dynamodb.create_email_index()
    dynamodb.add_dummy_users()
    return app

app = create_app()

