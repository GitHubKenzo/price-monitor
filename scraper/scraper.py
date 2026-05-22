import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_price(url: str) -> int:
    res = requests.get(url, headers=HEADERS, timeout=10)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")

    # 1. meta[itemprop="price"]（最優先）
    meta_price = soup.select_one('meta[itemprop="price"]')
    if meta_price and meta_price.get("content"):
        digits = re.sub(r"\D", "", meta_price["content"])
        if digits.isdigit():
            return int(digits)

    # 2. itemprop="price"
    itemprop_price = soup.select_one('[itemprop="price"]')
    if itemprop_price:
        text = itemprop_price.get_text(strip=True)
        digits = re.sub(r"\D", "", text)
        if digits.isdigit():
            return int(digits)

    # 3. 汎用クラス（フォールバック）
    candidates = soup.select(
        '[class*="Price"], [class*="price"], [class*="Value"], [class*="value"]'
    )

    for el in candidates:
        text = el.get_text(strip=True)
        digits = re.sub(r"\D", "", text)
        if digits.isdigit():
            return int(digits)

    raise ValueError("価格情報が取得できませんでした")
