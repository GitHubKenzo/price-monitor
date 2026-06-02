import sys
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


def test_main_retry_success(monkeypatch):
    monkeypatch.setattr(main, "init_db", lambda: None)
    monkeypatch.setattr(main, "SessionLocal", lambda: OneProductSession())

    call_count = {"count": 0}

    def fake_fetch(url):
        call_count["count"] += 1

        if call_count["count"] == 1:
            raise requests.exceptions.Timeout("timeout")

        return 12345

    monkeypatch.setattr(main, "fetch_price", fake_fetch)

    monkeypatch.setattr(main.time, "sleep", lambda x: None)

    monkeypatch.setattr(
        main,
        "save_price_if_changed",
        lambda session, product, price: None
    )

    monkeypatch.setattr(sys, "argv", ["main.py"])

    main.main()

    assert call_count["count"] == 2