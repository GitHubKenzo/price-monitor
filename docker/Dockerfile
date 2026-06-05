FROM python:3.10-slim

# 非 root ユーザ（UID/GID は compose 側で上書きされる）
RUN useradd -m appuser

WORKDIR /workspace

# -------------------------
# 依存インストール
# -------------------------
COPY app/scraper/requirements.txt /workspace/app/scraper/requirements.txt
RUN pip install --no-cache-dir -r /workspace/app/scraper/requirements.txt

# -------------------------
# アプリ本体
# -------------------------
# COPY app /workspace/app

# Python import 安定化
ENV PYTHONPATH=/workspace

# DB ディレクトリ
RUN mkdir -p /workspace/data

# デフォルトユーザ（UID/GID は compose で上書き）
USER appuser

# デフォルト起動
CMD ["python", "-m", "app.main"]
