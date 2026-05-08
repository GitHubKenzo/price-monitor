import os
import requests


LINE_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")


def notify(message: str):
    if not LINE_TOKEN:
        print(f"[NOTIFY] {message}")
        return

    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {LINE_TOKEN}"}
    data = {"message": message}

    try:
        res = requests.post(url, headers=headers, data=data, timeout=10)
        if res.status_code != 200:
            print(f"[NOTIFY-ERROR] status={res.status_code}, body={res.text}")
    except Exception as e:
        print(f"[NOTIFY-ERROR] {e}")
