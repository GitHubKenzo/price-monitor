from app.scraper import notifier
import requests

class DummyResponse:
    status_code = 500
    text = "server error"

def test_notify_error_mode(monkeypatch, capsys):
    # LINE_TOKEN を強制的にセット（dummy モードを回避）
    monkeypatch.setattr(notifier, "LINE_TOKEN", "DUMMY")

    # requests.post が例外を投げるようにする
    def raise_error(*args, **kwargs):
        raise Exception("boom")

    monkeypatch.setattr(requests, "post", raise_error)

    notifier.notify("hello")

    out = capsys.readouterr().out
    assert "[NOTIFY-ERROR] boom" in out


def test_notify_status_error2(monkeypatch, capsys):
    # real モードにするため LINE_TOKEN をセット
    monkeypatch.setattr(notifier, "LINE_TOKEN", "DUMMY")

    # requests.post が 500 を返すようにする
    monkeypatch.setattr(requests, "post", lambda *a, **k: DummyResponse())

    notifier.notify("hello")

    out = capsys.readouterr().out
    assert "[NOTIFY-ERROR] status=500, body=server error" in out
