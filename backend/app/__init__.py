from flask import Flask, request
from flask_cors import CORS
from flasgger import Swagger
from flask_caching import Cache
from app.database.connection import db
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

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
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300

    # Configuração do Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
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

    # Criação do banco de dados
    with app.app_context():
        db.create_all()

    # Registro dos blueprints
    from app.routes.products import products_bp
    from app.routes.automation_routes import automation_bp
    app.register_blueprint(products_bp)
    app.register_blueprint(automation_bp)
    
    # Inicialização da automação de preços (sem iniciar automaticamente)
    from app.services.price_automation import init_price_automation
    with app.app_context():
        app.price_automation = init_price_automation(app, interval=10, min_price_factor=0.8, max_price_factor=1.2)
        logger.info("Price automation initialized but not started")

    # Registro dos comandos CLI personalizados
    from app.commands import register_commands
    register_commands(app, db)
    
    # Adicionar headers para evitar cache em respostas dinâmicas
    @app.after_request
    def add_no_cache_headers(response):
        if 'products' in str(request.url_rule).lower() or 'automation' in str(request.url_rule).lower():
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
        return response

    logger.info("Flask app initialized")
    return app