from flask import Flask
from flask_cors import CORS
from flasgger import Swagger  
from app.database.connection import db
from app.services.price_automation import init_price_automation
from flask_caching import Cache

cors = CORS()
cache = Cache()

def create_app():
    """
    Cria e configura a aplicação Flask, incluindo banco de dados,
    CORS, documentação Swagger, blueprints e comandos CLI.
    
    Returns:
        app (Flask): Instância configurada da aplicação Flask.
    """
    app = Flask(__name__)
    
    # Configuração do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configuração do Cache usando Redis
    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_HOST'] = 'redis'
    app.config['CACHE_REDIS_PORT'] = 6379
    app.config['CACHE_REDIS_DB'] = 0
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # 5 minutos

    # Configuração do Swagger (documentação automática da API)
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,  # incluir todas as rotas
                "model_filter": lambda tag: True,  # incluir todos os modelos
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/swagger/"
    }
    Swagger(app, config=swagger_config)

    # Inicialização das extensões
    db.init_app(app)
    cors.init_app(app)
    cache.init_app(app)

    # Registro dos blueprints (rotas organizadas por funcionalidade)
    from app.routes.products import products_bp
    app.register_blueprint(products_bp)

    init_price_automation(app, interval=10)

    from app.routes.automation_routes import automation_bp
    app.register_blueprint(automation_bp)
    
    # Registro dos comandos CLI personalizados
    from app.commands import register_commands
    register_commands(app, db)
    
    return app
