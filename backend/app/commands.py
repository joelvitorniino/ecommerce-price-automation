import click
from app.models.product import Product, PriceHistory
from datetime import datetime, timedelta
import random

def register_commands(app, db): 
    """Register CLI commands with the Flask app."""
    
    @app.cli.command('init-db')
    def init_db_command():
        """Initialize the database."""
        with app.app_context():
            db.drop_all()
            db.create_all()
        click.echo('Database initialized!')

    @app.cli.command('seed-db')
    def seed_db_command():
        """Seed the database with sample data."""
        with app.app_context():
            db.create_all()
            
            products_data = [
                {
                    'name': 'Smartphone Samsung Galaxy',
                    'description': 'Smartphone Samsung Galaxy S21 com 128GB',
                    'original_price': 1200.00,
                    'category': 'Electronics',
                    'image_url': 'https://samsungbrshop.vtexassets.com/arquivos/ids/222466/image-147812a827ce414cbeecb5bb91eecb25-1-.jpg?v=638315272752900000'
                },
                {
                    'name': 'Notebook Lenovo IdeaPad',
                    'description': 'Notebook Lenovo IdeaPad 5 com 16GB RAM',
                    'original_price': 2500.00,
                    'category': 'Electronics',
                    'image_url': 'https://m.media-amazon.com/images/I/61LSRuuEwBL._AC_UF894,1000_QL80_.jpg'
                },
                {
                    'name': 'Fones Bluetooth JBL',
                    'description': 'Fones de ouvido Bluetooth JBL Tune 510BT',
                    'original_price': 350.00,
                    'category': 'Accessories',
                    'image_url': 'https://m.media-amazon.com/images/I/61kFL7ywsZS._AC_UF1000,1000_QL80_.jpg'
                },
                {
                    'name': 'Smartwatch Apple',
                    'description': 'Apple Watch Series 7 45mm',
                    'original_price': 2800.00,
                    'category': 'Wearables',
                    'image_url': 'https://m.media-amazon.com/images/I/51IOwTt4daL._AC_UF1000,1000_QL80_.jpg'
                },
                {
                    'name': 'Tablet iPad',
                    'description': 'Apple iPad 10.2" 64GB Wi-Fi',
                    'original_price': 1800.00,
                    'category': 'Tablets',
                    'image_url': 'https://cdn.awsli.com.br/2164/2164487/produto/154326297cec4b41c19.jpg'
                },
                {
                    'name': 'Câmera Canon DSLR',
                    'description': 'Câmera Canon EOS Rebel T7 DSLR',
                    'original_price': 3200.00,
                    'category': 'Cameras',
                    'image_url': 'https://m.media-amazon.com/images/I/61BKYlNqH6L._AC_UF894,1000_QL80_.jpg'
                }
            ]

            # Clear existing data
            PriceHistory.query.delete()
            Product.query.delete()
            
            # Add products
            for data in products_data:
                product = Product(
                    name=data['name'],
                    description=data['description'],
                    original_price=data['original_price'],
                    current_price=data['original_price'],
                    category=data['category'],
                    image_url=data['image_url']
                )
                db.session.add(product)

            db.session.commit()

            # Add price history
            products = Product.query.all()
            for product in products:
                for i in range(3):
                    price_history = PriceHistory(
                        product_id=product.id,
                        price=round(product.original_price * random.uniform(0.8, 1.2), 2),
                        timestamp=datetime.utcnow() - timedelta(hours=i * 3)
                    )
                    db.session.add(price_history)

            db.session.commit()
        click.echo('Database seeded with sample data!')