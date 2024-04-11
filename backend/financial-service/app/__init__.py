from flask import Flask, jsonify, request
from app import dynamodb, dummydata
from flask_cors import CORS


def create_app():
    app = Flask(__name__, static_folder='public',
            static_url_path='', template_folder='public')
    dynamodb.create_accounts_table()
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'claire.commerceshop@gmail.com'
    app.config['MAIL_PASSWORD'] = 'gddu rejb dxwk scsw'
    app.config['MAIL_DEFAULT_SENDER'] = 'claire.commerceshop@gmail.com'
    app.config['MAIL_MAX_EMAILS'] = None
    app.config['MAIL_ASCII_ATTACHMENTS'] = False
    CORS(app)
    return app

app = create_app()