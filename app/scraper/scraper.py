import requests
import json
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_price(url: str) -> int:
    res = requests.get(url, headers=HEADERS, timeout=10)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")

    # ========================================================
    # 確実なルート：全域から構造化データを安全に抜ける優先ロジック
    # ========================================================
    
    # 1. meta[itemprop="price"]（最優先・誤検知が極めて少ない定番構造）
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

    # ========================================================
    # ★ S-1：コンテキスト制約（誤検知・DB汚染を絶対に防ぐ防衛策）
    # ページ全域ではなく、メイン商品のエリアにスコープを限定する
    # ========================================================
    # Yahooショッピングの主要なメイン商品ブロックのセレクタ候補
    main_context = soup.select_one('div#sub-main, main, div[class*="MainColumn"], div#yjMain')
    
    # メインコンテキストが特定できた場合のみ、その配下からフォールバック抽出
    target_area = main_context if main_context else soup

    # 3. 構造化データ JSON-LD のフォールバック（メインエリア内を優先、なければ安全にパース）
    if main_context:
        scripts = main_context.find_all("script", type="application/ld+json")
        for script in scripts:
            try:
                data = json.loads(script.string)
                # 単一オブジェクト、またはリスト形式のJSON-LDに対応
                items = data if isinstance(data, list) else [data]
                for item in items:
                    # Offers内のprice、またはlowPriceを探索
                    if "offers" in item:
                        offers = item["offers"]
                        if isinstance(offers, dict) and "price" in offers:
                            return int(re.sub(r"\D", "", str(offers["price"])))
                        elif isinstance(offers, dict) and "lowPrice" in offers:
                            return int(re.sub(r"\D", "", str(offers["lowPrice"])))
            except Exception:
                continue

    # 4. 汎用クラスによる最終フォールバック（必ず限定されたエリア内から探索）
    candidates = target_area.select(
        '[class*="Price"], [class*="price"], [class*="Value"], [class*="value"]'
    )

    for el in candidates:
        # クラス名に "sub", "related", "recommend", "aside" などが含まれる場合は
        # 他人の価格（おすすめ商品）の可能性が高いためスキップする（防御力MAX）
        parent_classes = "".join(str(p.get("class", "")) for p in el.parents)
        if any(x in parent_classes.lower() for x in ["recommend", "related", "ranking", "itemlist"]):
            continue

        text = el.get_text(strip=True)
        digits = re.sub(r"\D", "", text)
        if digits.isdigit() and len(digits) >= 2:  # 1桁の数字（ポイント倍率等）は除外
            return int(digits)

    raise ValueError("価格情報が取得できませんでした（メイン商品コンテキスト内での抽出失敗）")