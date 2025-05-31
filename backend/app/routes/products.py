from flask import Blueprint, jsonify
from app.models.product import Product, PriceHistory

products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
def get_products():
    """
    Retorna a lista de produtos cadastrados.
    ---
    tags:
      - Produtos
    responses:
      200:
        description: Lista de produtos.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              description:
                type: string
              originalPrice:
                type: number
              currentPrice:
                type: number
              category:
                type: string
              image:
                type: string
              lastUpdate:
                type: string
    """
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'originalPrice': p.original_price,
        'currentPrice': p.current_price,
        'category': p.category,
        'image': p.image_url,
        'lastUpdate': p.updated_at.isoformat() if p.updated_at else None
    } for p in products])

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
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            description:
              type: string
            originalPrice:
              type: number
            currentPrice:
              type: number
            category:
              type: string
            image:
              type: string
            lastUpdate:
              type: string
    """
    product = Product.query.get_or_404(id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'originalPrice': product.original_price,
        'currentPrice': product.current_price,
        'category': product.category,
        'image': product.image_url,
        'lastUpdate': product.updated_at.isoformat() if product.updated_at else None
    })

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
        schema:
          type: array
          items:
            type: object
            properties:
              price:
                type: number
              timestamp:
                type: string
    """
    history = PriceHistory.query.filter_by(product_id=id).order_by(PriceHistory.timestamp.desc()).all()
    return jsonify([{
        'price': h.price,
        'timestamp': h.timestamp.isoformat()
    } for h in history])
