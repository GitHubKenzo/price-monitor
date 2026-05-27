import sys
from app import main

def test_main_as_script(monkeypatch, capsys):
    # __name__ を "__main__" に偽装
    monkeypatch.setattr(main, "__name__", "__main__")

    # init_db と SessionLocal をモック
    monkeypatch.setattr(main, "init_db", lambda: None)

    class DummySession:
        def query(self, model):
            class Q:
                def all(self_inner):
                    return []
            return Q()
        def close(self):
            pass

    monkeypatch.setattr(main, "SessionLocal", lambda: DummySession())

    monkeypatch.setattr(sys, "argv", ["main.py"])

    # __main__ ガードを直接通す
    main.main()

    out = capsys.readouterr().out
    assert "Start at" in out
