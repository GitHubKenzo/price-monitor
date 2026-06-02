import sys
from app import main

class OneProductSession:
    def query(self, model):
        class DummyQuery:
            def all(self_inner):
                class P:
                    name = "X"
                    url = "http://example.com"
                return [P()]
        return DummyQuery()

    def close(self):
        pass

def test_main_loop_exception(monkeypatch, capsys):
    monkeypatch.setattr(main, "init_db", lambda: None)
    monkeypatch.setattr(main, "SessionLocal", lambda: OneProductSession())

    # fetch_price が例外を投げる
    monkeypatch.setattr(main, "fetch_price", lambda url: (_ for _ in ()).throw(Exception("boom")))

    monkeypatch.setattr(sys, "argv", ["main.py"])

    main.main()

    out = capsys.readouterr().out
    assert "[ERROR] X: boom" in out
