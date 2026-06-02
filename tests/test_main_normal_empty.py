import sys
from app import main
import app.db.db as db_module

class EmptySession:
    def query(self, model):
        class DummyQuery:
            def all(self_inner):
                return []  # ★ 空リスト
        return DummyQuery()

def test_main_normal_empty(monkeypatch, capsys):
    # init_db を無効化
    monkeypatch.setattr(main, "init_db", lambda: None)

    # ★ main.SessionLocal ではなく import 元の SessionLocal をモックする
    monkeypatch.setattr(main, "SessionLocal", lambda: EmptySession())

    # 通常モード
    monkeypatch.setattr(sys, "argv", ["main.py"])

    main.main()

    out = capsys.readouterr().out

    assert "通常モード" in out
    assert "products テーブルが空です" in out  # ★ 未カバー行 50–51