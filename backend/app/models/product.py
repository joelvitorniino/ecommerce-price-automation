from datetime import datetime, timezone
from sqlalchemy import CheckConstraint, Index
from sqlalchemy.orm import validates
from app.database.connection import db

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text)
    original_price = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), index=True)
    image_url = db.Column(db.String(255), default='https://picsum.photos/300/200')
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    price_history = db.relationship('PriceHistory', backref='product', lazy='dynamic', cascade='all, delete-orphan')

    __table_args__ = (
        CheckConstraint('original_price >= 0', name='check_original_price_non_negative'),
        CheckConstraint('current_price >= 0', name='check_current_price_non_negative'),
        Index('ix_products_name_category', 'name', 'category'),
    )

    @validates('original_price', 'current_price')
    def validate_price(self, key, value):
        if value < 0:
            raise ValueError(f"{key} cannot be negative")
        return value

    @validates('image_url')
    def validate_image_url(self, key, value):
        if value and len(value) > 255:
            raise ValueError("Image URL is too long")
        return value or 'https://picsum.photos/300/200'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'original_price': self.original_price,
            'current_price': self.current_price,
            'category': self.category,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'last_update': self.updated_at.isoformat()
        }

class PriceHistory(db.Model):
    __tablename__ = 'price_history'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc), index=True)

    __table_args__ = (
        CheckConstraint('price >= 0', name='check_price_non_negative'),
        Index('ix_price_history_product_timestamp', 'product_id', 'timestamp'),
    )

    @validates('price')
    def validate_price(self, key, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        return value

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'price': self.price,
            'timestamp': self.timestamp.isoformat()
        }

    @classmethod
    def get_recent_history(cls, product_id: int, limit: int = 10):
        return cls.query.filter_by(product_id=product_id).order_by(cls.timestamp.desc()).limit(limit).all()