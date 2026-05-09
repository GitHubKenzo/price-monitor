from datetime import datetime
from db.db import init_db, SessionLocal
from db.models import Product
from db.logic import save_price_if_changed
from scraper.scraper import fetch_price
from utils import load_products_from_json  # あなたの既存関数

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

            # 価格変動ロジック（db/logic.py）
            save_price_if_changed(session, p, price)

        except Exception as e:
            print(f"[ERROR] {p.name}: {e}")

if __name__ == "__main__":
    main()
