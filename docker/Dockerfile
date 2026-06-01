FROM python:3.10-slim

# 作業ディレクトリ
WORKDIR /app

# -------------------------
# 1. 本番用依存のインストール（キャッシュ効率化）
# -------------------------
# 依存定義ファイルだけを先にコピーして、ソースコード変更時にレイヤーキャッシュが切れるのを防ぐ
COPY app/scraper/requirements.txt /app/scraper/requirements.txt

# 本番依存をインストール
RUN pip install --no-cache-dir -r /app/scraper/requirements.txt

# -------------------------
# 2. アプリ本体をコピー
# -------------------------
# プロジェクトルート（.）基準のビルドコンテキストから、app内をクリーンに転送
COPY app /app

# デフォルト CMD（scraper 用）
CMD ["python", "scraper/scraper.py"]