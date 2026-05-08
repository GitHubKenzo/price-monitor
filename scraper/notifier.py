import requests

def notify(message: str):
    url = "https://notify-api.line.me/api/notify"
    token = "YOUR_LINE_TOKEN"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"message": message}
    requests.post(url, headers=headers, data=data)
