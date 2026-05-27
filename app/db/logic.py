import logging
from datetime import datetime
from app.db.models import PriceHistory

logger = logging.getLogger(__name__)

def save_price_if_changed(session, product, new_price):
    last = (
        session.query(PriceHistory)
        .filter(PriceHistory.product_id == product.id)
        .order_by(PriceHistory.scraped_at.desc())
        .first()
    )

    if last is None or last.price != new_price:
        history = PriceHistory(product_id=product.id, price=new_price)
        session.add(history)
        session.commit()

        logger.info(f"Price changed! {product.name}: {new_price} 円")

    else:
        logger.info(f"No change: {product.name} は前回と同じ価格 {new_price} 円")
