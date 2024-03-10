from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

def create_app(configName='config'):
    app = Flask(__name__)
    app.config.from_object(configName)
    db.init_app(app)
    migrate.init_app(app, db)
    return app

app = create_app()

from app import routes, models
from app.routes import user_api_blueprint

with app.app_context():
    db.create_all()
    app.register_blueprint(user_api_blueprint, url_prefix='/user_api')

