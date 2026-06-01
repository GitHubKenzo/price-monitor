import sys
import time
import requests
import logging
from db.db import init_db, SessionLocal
from db.models import Product
from db.logic import save_price_if_changed
from scraper.scraper import fetch_price
from utils import load_products_from_json
from datetime import datetime
import argparse

# ロガーの設定（既存のロギング環境に合わせる）
logger = logging.getLogger("price_monitor")

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
    # ここから従来の処理 ＋ 【S-2: リトライ機構】
    # -----------------------------
    products = session.query(Product).all()
    if not products:
        print("[WARN] products テーブルが空です")
        return

    for p in products:
        price = None
        # 1回目の試行
        try:
            price = fetch_price(p.url)
        except requests.exceptions.RequestException as e:
            # ネットワーク瞬断やタイムアウト時は5秒待って1回だけリトライ
            print(f"[WARN] Temporary network error for {p.name}. Retrying in 5 seconds... (Error: {e})")
            time.sleep(5)
            try:
                price = fetch_price(p.url)
            except Exception as retry_error:
                # 2回目も失敗した場合は、既存の確実な詳細ログを出力してスキップ
                logger.error(f"Error checking {p.name} after retry: {retry_error}", exc_info=True)
                continue
        except Exception as e:
            # その他の致命的な例外（パースエラー等）は即座にロギングしてスキップ
            logger.error(f"Error checking {p.name}: {e}", exc_info=True)
            continue

        # 価格が正常に取得できた場合のみ保存処理に移行
        if price is not None:
            print(f"[INFO] {p.name}: {price} 円")
            # 価格変動ロジック（db/logic.py）
            save_price_if_changed(session, p, price)

    print("[INFO] Scraper finished")

if __name__ == "__main__":  # pragma: no cover
    main()