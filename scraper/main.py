from db import SessionLocal, Product, PriceHistory
from scraper import fetch_price
from notifier import notify

def main():
    session = SessionLocal()
    products = session.query(Product).all()

    for p in products:
        price = fetch_price(p.url)

        # 保存
        history = PriceHistory(product_id=p.id, price=price)
        session.add(history)
        session.commit()

        # 前回価格と比較
        last_two = (
            session.query(PriceHistory)
            .filter(PriceHistory.product_id == p.id)
            .order_by(PriceHistory.scraped_at.desc())
            .limit(2)
            .all()
        )

        if len(last_two) == 2 and last_two[0].price != last_two[1].price:
            notify(f"{p.name} の価格が変動しました: {last_two[0].price}円")

if __name__ == "__main__":
    main()
