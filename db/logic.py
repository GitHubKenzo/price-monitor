from datetime import datetime
from db.models import PriceHistory

def save_price_if_changed(session, product, new_price):
    # 直近の価格を取得
    last = (
        session.query(PriceHistory)
        .filter(PriceHistory.product_id == product.id)
        .order_by(PriceHistory.scraped_at.desc())
        .first()
    )

    # 初回 or 価格変動あり
    if last is None or last.price != new_price:
        history = PriceHistory(product_id=product.id, price=new_price)
        session.add(history)
        session.commit()

        print(f"[INFO] Price changed! {product.name}: {new_price} 円")

        # 通知（後で実装）
        # notify(f"{product.name} の価格が変動しました: {new_price}円（前回: {last.price if last else '初回'}円）")

    else:
        print(f"[INFO] No change: {product.name} は前回と同じ価格 {new_price} 円")
