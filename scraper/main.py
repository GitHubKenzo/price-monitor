import json
import os
from datetime import datetime

from db import SessionLocal, Product, PriceHistory, init_db
from scraper import fetch_price
from notifier import notify


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_JSON = os.path.join(BASE_DIR, "products.json")


def load_products_from_json(session):
    if not os.path.exists(PRODUCTS_JSON):
        print(f"[WARN] products.json が見つかりません: {PRODUCTS_JSON}")
        return

    with open(PRODUCTS_JSON, "r", encoding="utf-8") as f:
        products = json.load(f)

    for p in products:
        exists = (
            session.query(Product)
            .filter(Product.url == p["url"])
            .first()
        )
        if not exists:
            session.add(Product(name=p["name"], url=p["url"]))
            print(f"[INIT] 追加: {p['name']}")
    session.commit()


def main():
    print(f"[INFO] Start at {datetime.now()}")
    init_db()
    session = SessionLocal()

    # 初回起動時に products.json から DB に登録
    load_products_from_json(session)

    products = session.query(Product).all()
    if not products:
        print("[WARN] products テーブルが空です")
        return

    for p in products:
        try:
            price = fetch_price(p.url)
            print(f"[INFO] {p.name}: {price} 円")

            history = PriceHistory(product_id=p.id, price=price)
            session.add(history)
            session.commit()

            last_two = (
                session.query(PriceHistory)
                .filter(PriceHistory.product_id == p.id)
                .order_by(PriceHistory.scraped_at.desc())
                .limit(2)
                .all()
            )

            if len(last_two) == 2 and last_two[0].price != last_two[1].price:
                msg = f"{p.name} の価格が変動しました: {last_two[0].price}円（前回: {last_two[1].price}円）"
                notify(msg)

        except Exception as e:
            print(f"[ERROR] {p.name}: {e}")

    session.close()
    print(f"[INFO] End at {datetime.now()}")


if __name__ == "__main__":
    main()
