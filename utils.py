import json
from db.models import Product

def load_products_from_json(session, path="products.json"):
    """products.json を読み込み、DB に存在しない商品だけ追加する"""
    with open(path, "r", encoding="utf-8") as f:
        products = json.load(f)

    for p in products:
        exists = session.query(Product).filter(Product.url == p["url"]).first()
        if not exists:
            new_p = Product(name=p["name"], url=p["url"])
            session.add(new_p)
            session.commit()
            print(f"[INFO] Added product: {p['name']}")

def notify(message, token_path="line_token.txt"):
    """【将来の拡張用】LINE/Discord/Slack等の通知を一元管理するダミー実装"""
    # 現状は line_token.txt を読み込むシンプルな実装
    with open(token_path, "r") as f:
        token = f.read().strip()

    import requests
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"message": message}

    res = requests.post(url, headers=headers, data=data)
    print(f"[INFO] LINE Notify status: {res.status_code}")