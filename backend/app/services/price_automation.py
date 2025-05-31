from app.models.product import Product, PriceHistory
from app.database.connection import db
import random
from datetime import datetime
import time
from threading import Thread

automation_active = False

def update_prices(app):
    global automation_active
    with app.app_context():
        while automation_active:
            try:
                products = Product.query.all()
                for product in products:
                    new_price = round(product.original_price * random.uniform(0.8, 1.2), 2)
                    product.current_price = new_price

                    history = PriceHistory(
                        product_id=product.id,
                        price=new_price,
                        timestamp=datetime.utcnow()
                    )
                    db.session.add(history)
                db.session.commit()
                print(f"Prices updated at {datetime.utcnow()}")
            except Exception as e:
                print(f"Error updating prices: {e}")
            time.sleep(10)

def start_automation(app=None):
    global automation_active
    if not automation_active and app is not None:
        automation_active = True
        thread = Thread(target=update_prices, args=(app,))
        thread.daemon = True
        thread.start()
        return True
    return False

def stop_automation():
    global automation_active
    automation_active = False
    return True

def get_automation_status():
    return automation_active
