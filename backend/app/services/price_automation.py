from threading import Thread, Event, Lock
import logging
from datetime import datetime, timezone
from typing import Optional
from flask import Flask
from sqlalchemy.exc import SQLAlchemyError
from app.database.connection import db
import random

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class PriceAutomation:
    def __init__(self, app: Flask, interval: float = 10, min_price_factor: float = 0.8, max_price_factor: float = 1.2):
        self.app = app
        self.interval = interval
        self.min_price_factor = min_price_factor
        self.max_price_factor = max_price_factor
        self._stop_event = Event()
        self._thread: Optional[Thread] = None
        self._lock = Lock()
        self._last_update: Optional[datetime] = None
        self._update_count = 0
        self._error_count = 0

    def _update_prices_loop(self):
        # Defer imports to avoid circular dependency
        from app.models.product import Product, PriceHistory
        while not self._stop_event.is_set():
            with self.app.app_context():
                try:
                    with self._lock:
                        logger.debug("Starting price update cycle")
                        products = Product.query.all()
                        price_histories = []
                        updated_products = 0

                        for product in products:
                            # Pular produtos com preço original inválido
                            if product.original_price <= 0:
                                logger.debug(f"Skipping product {product.id} with original_price <= 0")
                                continue
                            
                            # Calcular limites
                            min_price = round(product.original_price * self.min_price_factor, 2)
                            max_price = round(product.original_price * self.max_price_factor, 2)
                            
                            # Garantir min <= max
                            if min_price > max_price:
                                min_price, max_price = max_price, min_price
                            
                            # Pular se não houver variação possível
                            if min_price == max_price:
                                logger.debug(f"Skipping product {product.id} because min_price == max_price")
                                continue
                            
                            # Usar gerador criptográfico para maior aleatoriedade
                            secure_random = random.SystemRandom()
                            new_price = None
                            max_attempts = 100
                            
                            # Tentar gerar preço diferente do atual
                            for _ in range(max_attempts):
                                candidate = round(secure_random.uniform(min_price, max_price), 2)
                                if candidate != product.current_price:
                                    new_price = candidate
                                    break
                            
                            # Fallback estratégico se ainda for igual
                            if new_price is None or new_price == product.current_price:
                                # Escolher o limite oposto ao preço atual
                                if product.current_price == min_price:
                                    new_price = max_price
                                else:
                                    new_price = min_price
                                logger.debug(f"Used fallback pricing for product {product.id}")
                            
                            # Atualizar produto
                            logger.debug(f"Updating product {product.id}: current={product.current_price}, new={new_price}, original={product.original_price}")
                            product.current_price = new_price
                            product.updated_at = datetime.now(timezone.utc)
                                                        
                            history = PriceHistory(
                                product_id=product.id,
                                price=new_price,
                                timestamp=datetime.now(timezone.utc)
                            )
                            price_histories.append(history)
                            updated_products += 1
                            

                        if updated_products > 0:
                            db.session.bulk_save_objects(price_histories)
                            db.session.commit()
                            self._last_update = datetime.now(timezone.utc)
                            self._update_count += 1
                            logger.info(f"Prices updated for {updated_products}/{len(products)} products at {self._last_update.isoformat()}")
                        else:
                            logger.info(f"No products found to update at {datetime.now(timezone.utc).isoformat()}")

                except SQLAlchemyError as e:
                    db.session.rollback()
                    self._error_count += 1
                    logger.error(f"Database error updating prices: {str(e)}")
                except Exception as e:
                    db.session.rollback()
                    self._error_count += 1
                    logger.error(f"Unexpected error updating prices: {str(e)}")

            # Aguarda o intervalo antes da próxima iteração
            self._stop_event.wait(self.interval)

    def start(self) -> bool:
        with self._lock:
            if self._thread is None or not self._thread.is_alive():
                self._stop_event.clear()
                self._thread = Thread(target=self._update_prices_loop, daemon=True)
                self._thread.start()
                logger.info("Price automation started.")
                return True
            logger.warning("Price automation is already running.")
            return False

    def stop(self) -> bool:
        with self._lock:
            if self._thread and self._thread.is_alive():
                self._stop_event.set()
                self._thread.join()
                self._thread = None
                logger.info("Price automation stopped.")
                return True
            logger.info("Price automation is not running.")
            return False

    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def get_status(self) -> dict:
        return {
            "is_running": self.is_running(),
            "last_update": self._last_update.isoformat() if self._last_update else None,
            "update_count": self._update_count,
            "error_count": self._error_count,
            "interval": self.interval,
            "price_range": {
                "min_factor": self.min_price_factor,
                "max_factor": self.max_price_factor
            }
        }

    def set_interval(self, interval: float) -> None:
        with self._lock:
            if interval > 0:
                self.interval = interval
                logger.info(f"Price update interval set to {interval} seconds.")
            else:
                logger.error("Interval must be positive.")

    def set_price_range(self, min_factor: float, max_factor: float) -> None:
        with self._lock:
            if 0 <= min_factor <= max_factor:
                self.min_price_factor = min_factor
                self.max_price_factor = max_factor
                logger.info(f"Price range set to {min_factor*100}% - {max_factor*100}% of original price.")
            else:
                logger.error("Invalid price range: min_factor must be non-negative and <= max_factor.")

# Instância singleton
price_automation: Optional[PriceAutomation] = None

def init_price_automation(app: Flask, interval: float = 10, min_price_factor: float = 0.8, max_price_factor: float = 1.2) -> PriceAutomation:
    global price_automation
    with Lock():
        if price_automation is None:
            price_automation = PriceAutomation(app, interval, min_price_factor, max_price_factor)
        return price_automation