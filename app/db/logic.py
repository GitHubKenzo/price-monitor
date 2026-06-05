#import logging
from app.db.models import PriceHistory
from app.logger import logger

#logger = logging.getLogger(__name__)

def save_price(session, product, new_price):
    last = (
        session.query(PriceHistory)
        .filter(PriceHistory.product_id == product.id)
        .order_by(PriceHistory.scraped_at.desc())
        .first()
    )
    # 価格履歴を保存
    history = PriceHistory(product_id=product.id, price=new_price)
    session.add(history)
    session.commit()
    # 価格変動のログ出力
    if last is None or last.price != new_price:
        logger.info(f"Price changed! {product.name}: {new_price} 円")
        
    else:
        logger.info(f"No change: {product.name} は前回と同じ価格 {new_price} 円")

