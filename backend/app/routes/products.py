from flask import Blueprint, jsonify
from app.database.connection import db
from app.models.product import Product

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    product_list = [{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'original_price': p.original_price,
        'current_price': p.current_price,
        'category': p.category
    } for p in products]
    return jsonify(product_list)
