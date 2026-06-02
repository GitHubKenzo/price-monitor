import sys
from app import main

# ダミー Product
class DummyProduct:
    def __init__(self):
        self.name = "Dummy"
        self.url = "http://example.com"

# ダミー Session
class DummySession:
    def query(self, model):
        class DummyQuery:
            def all(self_inner):
                return [DummyProduct()]  # ★ 1件返す
        return DummyQuery()

    def close(self):
        pass


def test_main_init_branch(monkeypatch, capsys):
    # init_db を無効化
    monkeypatch.setattr(main, "init_db", lambda: None)

    # SessionLocal をダミーに
    monkeypatch.setattr(main, "SessionLocal", lambda: DummySession())

    # load_products_from_json が呼ばれたか確認するためのフラグ
    called = {"value": False}

    def fake_load_products(session):
        called["value"] = True

    monkeypatch.setattr(main, "load_products_from_json", fake_load_products)

    # fetch_price / save_price_if_changed は何もしない
    monkeypatch.setattr(main, "fetch_price", lambda url: 1234)
    monkeypatch.setattr(main, "save_price_if_changed", lambda s, p, price: None)

    # --init モードで実行
    monkeypatch.setattr(sys, "argv", ["main.py", "--init"])

    main.main()

    captured = capsys.readouterr()

    # ★ 未カバー行①：--init モードのメッセージ
    assert "--init モード" in captured.out

    # ★ 未カバー行②：load_products_from_json が呼ばれた
    assert called["value"] is True

    # ★ 未カバー行③：最後の Scraper finished
    assert "Scraper finished" in captured.out
