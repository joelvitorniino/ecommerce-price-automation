from datetime import datetime, timezone
from sqlalchemy import CheckConstraint
from app.database.connection import db

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)  # index adicionado
    description = db.Column(db.Text)
    original_price = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), index=True)  # index adicionado
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    price_history = db.relationship('PriceHistory', backref='product', lazy=True)

    __table_args__ = (
        CheckConstraint('original_price >= 0', name='check_original_price_non_negative'),
        CheckConstraint('current_price >= 0', name='check_current_price_non_negative'),
    )


class PriceHistory(db.Model):
    __tablename__ = 'price_history'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)  # index adicionado
    price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    __table_args__ = (
        CheckConstraint('price >= 0', name='check_price_non_negative'),
    )
