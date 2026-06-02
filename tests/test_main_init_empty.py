import sys
from app import main

class EmptySession:
    def query(self, model):
        class DummyQuery:
            def all(self_inner):
                return []  # ★ 空リストを返す
        return DummyQuery()

def test_main_init_empty(monkeypatch, capsys):
    monkeypatch.setattr(main, "init_db", lambda: None)
    monkeypatch.setattr(main, "SessionLocal", lambda: EmptySession())

    called = {"value": False}
    monkeypatch.setattr(main, "load_products_from_json", lambda s: called.update(value=True))

    monkeypatch.setattr(sys, "argv", ["main.py", "--init"])

    main.main()

    out = capsys.readouterr().out

    assert "--init モード" in out
    assert called["value"] is True
    assert "products テーブルが空です" in out  # ★ 未カバー行③
