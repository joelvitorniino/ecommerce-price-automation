from flask import Flask
from flask_cors import CORS
from app.database.connection import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app)

    db.init_app(app)

    from app.routes.products import products_bp
    app.register_blueprint(products_bp, url_prefix='/products')

    return app
