import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.scraper import notifier

def test_notify_dummy_mode(monkeypatch, capsys):
    # LINE_TOKEN を未設定にする
    monkeypatch.setattr(notifier, "LINE_TOKEN", None)

    notifier.notify("hello")

    captured = capsys.readouterr()
    assert "[NOTIFY] hello" in captured.out


def test_notify_real_mode(requests_mock, monkeypatch):
    # LINE_TOKEN を設定
    monkeypatch.setattr(notifier, "LINE_TOKEN", "DUMMY_TOKEN")

    # LINE Notify API をモック
    url = "https://notify-api.line.me/api/notify"
    requests_mock.post(url, status_code=200)

    notifier.notify("hello")

    # モックが呼ばれたか確認
    assert requests_mock.called
    req = requests_mock.request_history[0]
    assert req.url == url
    assert req.method == "POST"
    assert req.text == "message=hello"
