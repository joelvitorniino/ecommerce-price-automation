from app.models.product import Product, PriceHistory
from app.database.connection import db
import random
from datetime import datetime
from threading import Thread, Event

class PriceAutomation:
    def __init__(self, app, interval=10):
        self.app = app
        self.interval = interval
        self._stop_event = Event()
        self._thread = None

    def _update_prices_loop(self):
        with self.app.app_context():
            while not self._stop_event.is_set():
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
                    print(f"[{datetime.utcnow()}] Prices updated successfully.")
                except Exception as e:
                    db.session.rollback()
                    print(f"[{datetime.utcnow()}] Error updating prices: {e}")

                self._stop_event.wait(self.interval)

    def start(self):
        if self._thread is None or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = Thread(target=self._update_prices_loop, daemon=True)
            self._thread.start()
            print("Price automation started.")
            return True
        else:
            print("Price automation is already running.")
            return False

    def stop(self):
        if self._thread and self._thread.is_alive():
            self._stop_event.set()
            self._thread.join()
            print("Price automation stopped.")
            return True
        return False

    def is_running(self):
        return self._thread is not None and self._thread.is_alive()


# Singleton para toda a aplicação
price_automation = None

def init_price_automation(app, interval=10):
    global price_automation
    if price_automation is None:
        price_automation = PriceAutomation(app, interval)
    return price_automation
