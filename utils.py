import json
import requests

import json
import requests

def load_products_from_json(session, path="products.json"):
    """products.json を読み込み、DB に存在しない商品だけ追加する"""
    with open(path, "r", encoding="utf-8") as f:
        products = json.load(f)

    from db.models import Product

    for p in products:
        exists = session.query(Product).filter(Product.url == p["url"]).first()
        if not exists:
            new_p = Product(name=p["name"], url=p["url"])
            session.add(new_p)
            session.commit()
            print(f"[INFO] Added product: {p['name']}")

def notify(message, token_path="line_token.txt"):
    """LINE Notify でメッセージを送る"""
    with open(token_path, "r") as f:
        token = f.read().strip()

    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"message": message}

    res = requests.post(url, headers=headers, data=data)
    print(f"[INFO] LINE Notify status: {res.status_code}")


def notify(message, token_path="line_token.txt"):
    """LINE Notify でメッセージを送る"""
    with open(token_path, "r") as f:
        token = f.read().strip()

    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"message": message}

    res = requests.post(url, headers=headers, data=data)
    print(f"[INFO] LINE Notify status: {res.status_code}")
