import click
from datetime import datetime, timedelta, timezone
import random
from app.models.product import Product, PriceHistory

# Dados fixos de produtos
PRODUCTS_DATA = [
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

def register_commands(app, db):
    """
    Register custom CLI commands with the Flask app.
    """

    @app.cli.command('init-db')
    def init_db_command():
        """
        Drop and recreate all database tables.
        """
        try:
            with app.app_context():
                db.drop_all()
                db.create_all()
            click.echo('✅ Database initialized!')
        except Exception as e:
            click.echo(f'❌ Error initializing database: {e}', err=True)

    @app.cli.command('seed-db')
    def seed_db_command():
        """
        Seed the database with sample products and price history.
        """
        try:
            with app.app_context():
                db.create_all()
                clear_data(db)
                add_sample_products(db)
                generate_price_history(db)
            click.echo('✅ Database seeded with sample data!')
        except Exception as e:
            click.echo(f'❌ Error seeding database: {e}', err=True)


def clear_data(db):
    """
    Delete existing products and price history from the database.
    """
    try:
        PriceHistory.query.delete()
        Product.query.delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f'Failed to clear data: {e}') from e


def add_sample_products(db):
    """
    Add predefined products to the database.
    """
    try:
        for data in PRODUCTS_DATA:
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
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f'Failed to add sample products: {e}') from e


def generate_price_history(db):
    """
    Generate fake price history for all products.
    """
    try:
        products = Product.query.all()
        for product in products:
            for i in range(3):
                price = round(product.original_price * random.uniform(0.8, 1.2), 2)
                timestamp = datetime.now(timezone.utc) - timedelta(hours=i * 3)
                history = PriceHistory(
                    product_id=product.id,
                    price=price,
                    timestamp=timestamp
                )
                db.session.add(history)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f'Failed to generate price history: {e}') from e