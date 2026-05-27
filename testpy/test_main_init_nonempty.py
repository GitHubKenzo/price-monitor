import sys
from app import main

class DummyProduct:
    def __init__(self):
        self.name = "Dummy"
        self.url = "http://example.com"

class OneProductSession:
    def query(self, model):
        class DummyQuery:
            def all(self_inner):
                return [DummyProduct()]  # ★ 1件返す
        return DummyQuery()

def test_main_init_nonempty(monkeypatch, capsys):
    monkeypatch.setattr(main, "init_db", lambda: None)
    monkeypatch.setattr(main, "SessionLocal", lambda: OneProductSession())

    monkeypatch.setattr(main, "load_products_from_json", lambda s: None)
    monkeypatch.setattr(main, "fetch_price", lambda url: 1234)
    monkeypatch.setattr(main, "save_price_if_changed", lambda s, p, price: None)

    monkeypatch.setattr(sys, "argv", ["main.py", "--init"])

    main.main()

    out = capsys.readouterr().out

    assert "--init モード" in out
    assert "Scraper finished" in out  # ★ 未カバー行④
