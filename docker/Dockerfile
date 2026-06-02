FROM python:3.10-slim

WORKDIR /workspace

# -------------------------
# 依存インストール
# -------------------------
COPY app/scraper/requirements.txt /workspace/app/scraper/requirements.txt

RUN pip install --no-cache-dir -r /workspace/app/scraper/requirements.txt

# -------------------------
# アプリ本体
# -------------------------
COPY app /workspace/app

# Python import 安定化
ENV PYTHONPATH=/workspace
RUN mkdir -p /workspace/data

# デフォルト起動
CMD ["python", "-m", "app.main"]