import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.scraper.scraper import fetch_price
import pytest

def test_fetch_price_meta(monkeypatch):
    """meta[itemprop=price] がある場合のテスト"""

    class MockResponse:
        status_code = 200
        text = """
        <html>
            <head>
                <meta itemprop="price" content="1234" />
            </head>
        </html>
        """

        def raise_for_status(self):
            pass

    def mock_get(url, headers=None, timeout=10):
        return MockResponse()

    # requests.get をモックする
    monkeypatch.setattr("requests.get", mock_get)

    price = fetch_price("http://example.com")
    assert price == 1234
def test_fetch_price_itemprop(monkeypatch):
    """itemprop='price' の場合のテスト"""

    class MockResponse:
        status_code = 200
        text = """
        <html>
            <body>
                <span itemprop="price">¥2,345</span>
            </body>
        </html>
        """

        def raise_for_status(self):
            pass

    def mock_get(url, headers=None, timeout=10):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)

    price = fetch_price("http://example.com")
    assert price == 2345
def test_fetch_price_fallback(monkeypatch):
    """汎用クラス（price / Price / value / Value）から取得するテスト"""

    class MockResponse:
        status_code = 200
        text = """
        <html>
            <body>
                <div class="productPrice">3,456円</div>
            </body>
        </html>
        """

        def raise_for_status(self):
            pass

    def mock_get(url, headers=None, timeout=10):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)

    price = fetch_price("http://example.com")
    assert price == 3456


def test_fetch_price_not_found(monkeypatch):
    """価格が見つからない場合に ValueError が発生するテスト"""

    class MockResponse:
        status_code = 200
        text = """
        <html>
            <body>
                <div>No price here</div>
            </body>
        </html>
        """

        def raise_for_status(self):
            pass

    def mock_get(url, headers=None, timeout=10):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)

    with pytest.raises(ValueError):
        fetch_price("http://example.com")
