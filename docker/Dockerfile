FROM python:3.10-slim

# 作業ディレクトリ
WORKDIR /app

# -------------------------
# 1. 本番用依存のインストール
# -------------------------
# scraper の requirements をコピー
COPY ../app/scraper/requirements.txt /app/scraper/requirements.txt

# 本番依存をインストール
RUN pip install --no-cache-dir -r /app/scraper/requirements.txt

# -------------------------
# 2. テスト用依存のインストール
# -------------------------
# testpy の requirements をコピー
COPY ../testpy/requirements.txt /app/testpy/requirements.txt

# テスト依存（pytest など）をインストール
RUN pip install --no-cache-dir -r /app/testpy/requirements.txt

# -------------------------
# 3. アプリ本体をコピー
# -------------------------
COPY ../app /app

# デフォルト CMD（scraper 用）
CMD ["python", "scraper/scraper.py"]
