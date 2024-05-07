from flask import Flask
from app import dynamodb
from flask_cors import CORS
from app.routes import route_blueprint

def create_app():
    app = Flask(__name__, static_folder='public',
            static_url_path='', template_folder='public')
    app.register_blueprint(route_blueprint)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'claire.commerceshop@gmail.com'
    app.config['MAIL_PASSWORD'] = 'koso hxam kfjj swqv'
    app.config['MAIL_DEFAULT_SENDER'] = 'claire.commerceshop@gmail.com'
    app.config['MAIL_MAX_EMAILS'] = None
    app.config['MAIL_ASCII_ATTACHMENTS'] = False
    CORS(app)
    return app


app = create_app()


with app.app_context():
    dynamodb.create_accounts_table()



