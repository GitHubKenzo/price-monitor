import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def fetch_price(url: str) -> int:
    res = requests.get(url, headers=HEADERS, timeout=10)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")

    selectors = [
        ".elPrice",          # 通常価格
        ".elPriceNumber",    # 数値のみ
        ".elPriceValue",     # 別パターン
        ".elPrice__value",   # 新UI
    ]

    price_text = None

    for sel in selectors:
        el = soup.select_one(sel)
        if el and el.text.strip():
            price_text = el.text.strip()
            break

    if not price_text:
        raise ValueError("価格情報が取得できませんでした")

    digits = (
        price_text.replace(",", "")
        .replace("円", "")
        .replace("税込", "")
        .strip()
    )

    if not digits.isdigit():
        raise ValueError(f"価格の数値化に失敗しました: {price_text}")

    return int(digits)
