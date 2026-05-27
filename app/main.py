import sys
from db.db import init_db, SessionLocal
from db.models import Product
from db.logic import save_price_if_changed
from scraper.scraper import fetch_price
from utils import load_products_from_json
from datetime import datetime


import argparse

def main():
    print(f"[INFO] Start at {datetime.now()}")
    init_db()
    session = SessionLocal()

    # -----------------------------
    # ★ C-1 対応：--init のときだけ JSON を読み込む
    # -----------------------------
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--init",
        action="store_true",
        help="初回のみ products.json を DB に取り込む"
    )
    args = parser.parse_args()

    if args.init:
        print("[INFO] --init モード: products.json を DB に取り込みます")
        load_products_from_json(session)
    else:
        print("[INFO] 通常モード: JSON 取り込みはスキップします")

    # -----------------------------
    # ここから従来の処理
    # -----------------------------
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

    print("[INFO] Scraper finished")

if __name__ == "__main__":  # pragma: no cover
    main()
