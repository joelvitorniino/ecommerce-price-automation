from flask import Flask
from flask_cors import CORS
from flasgger import Swagger  
from app.database.connection import db

cors = CORS()

def create_app():
    app = Flask(__name__)
    
    # Configuração do banco
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,  # inclui todas as rotas
                "model_filter": lambda tag: True,  # inclui todos os modelos
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/swagger/"
    }
    Swagger(app, config=swagger_config)

    # Inicializa extensões
    db.init_app(app)
    cors.init_app(app)

    # Registra blueprints
    from app.routes.products import products_bp
    app.register_blueprint(products_bp)

    from app.routes.automation_routes import automation_bp
    app.register_blueprint(automation_bp)

    # Registra comandos
    from app.commands import register_commands
    register_commands(app, db)
    
    return app
