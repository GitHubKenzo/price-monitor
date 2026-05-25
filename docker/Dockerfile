FROM python:3.10-slim

WORKDIR /app

# app ディレクトリを丸ごとコピー
COPY ./app /app

# 依存関係インストール
RUN pip install --no-cache-dir -r /app/scraper/requirements.txt

CMD ["python", "/app/main.py"]
