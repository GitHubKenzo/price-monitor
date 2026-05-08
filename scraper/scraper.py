import requests
from bs4 import BeautifulSoup

def fetch_price(url: str) -> int:
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")

    # サイトに合わせて調整
    price_text = soup.select_one(".price").text
    price = int(price_text.replace(",", "").replace("円", ""))

    return price
