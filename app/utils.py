import json
from app.db.models import Product

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

