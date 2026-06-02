import sys
import logging
import requests
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


def test_main_retry_failed(monkeypatch, caplog):
    monkeypatch.setattr(main, "init_db", lambda: None)
    monkeypatch.setattr(main, "SessionLocal", lambda: OneProductSession())

    def fake_fetch(url):
        raise requests.exceptions.Timeout("timeout")

    monkeypatch.setattr(main, "fetch_price", fake_fetch)

    monkeypatch.setattr(main.time, "sleep", lambda x: None)

    monkeypatch.setattr(sys, "argv", ["main.py"])

    with caplog.at_level(logging.ERROR):
        main.main()

    assert "after retry" in caplog.text