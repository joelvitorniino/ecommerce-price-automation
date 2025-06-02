from flask import Blueprint, jsonify, abort, make_response
from app.models.product import Product, PriceHistory
from sqlalchemy.exc import SQLAlchemyError
from app.database.connection import db
from app import cache
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

products_bp = Blueprint('products', __name__)

def serialize_product(product):
    return {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'originalPrice': product.original_price,
        'currentPrice': product.current_price,
        'category': product.category,
        'imageUrl': product.image_url,
        'lastUpdate': product.updated_at.isoformat() if product.updated_at else None
    }

def serialize_price_history(history):
    return {
        'price': history.price,
        'timestamp': history.timestamp.isoformat()
    }

@products_bp.route('/products', methods=['GET'])
@cache.cached(timeout=0)  # Disable caching for this endpoint
def get_products():
    """
    Retorna a lista de produtos cadastrados.
    ---
    tags:
      - Produtos
    responses:
      200:
        description: Lista de produtos.
    """
    try:
        logger.debug("Fetching products from database")
        products = Product.query.all()
        serialized = [serialize_product(p) for p in products]
        logger.info(f"Returning {len(serialized)} products")
        response = make_response(jsonify(serialized), 200)
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching products: {str(e)}")
        return jsonify({'error': 'Erro ao buscar produtos', 'details': str(e)}), 500

@products_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    """
    Retorna os detalhes de um produto específico.
    ---
    tags:
      - Produtos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do produto
    responses:
      200:
        description: Detalhes do produto.
      404:
        description: Produto não encontrado.
    """
    try:
        product = db.session.get(Product, id)
        if not product:
            abort(404, description="Produto não encontrado")
        return jsonify(serialize_product(product)), 200
    except SQLAlchemyError as e:
        return jsonify({'error': 'Erro ao buscar produto', 'details': str(e)}), 500

@products_bp.route('/products/<int:id>/history', methods=['GET'])
def get_product_history(id):
    """
    Retorna o histórico de preços de um produto.
    ---
    tags:
      - Produtos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do produto
    responses:
      200:
        description: Histórico de preços.
      404:
        description: Produto não encontrado.
    """
    try:
        product = db.session.get(Product, id)
        if not product:
            abort(404, description="Produto não encontrado")

        history = PriceHistory.query.filter_by(product_id=id).order_by(PriceHistory.timestamp.desc()).all()
        serialized = [serialize_price_history(h) for h in history]
        return jsonify(serialized), 200
    except SQLAlchemyError as e:
        return jsonify({'error': 'Erro ao buscar histórico de preços', 'details': str(e)}), 500