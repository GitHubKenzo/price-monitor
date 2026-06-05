FROM python:3.10-slim

RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

# 非 root ユーザ（UID/GID は compose 側で上書き）
RUN useradd -m appuser

WORKDIR /workspace

# scraper と同じ依存関係を入れる
COPY ../app/scraper/requirements.txt /workspace/app/scraper/requirements.txt
RUN pip install --no-cache-dir -r /workspace/app/scraper/requirements.txt

# COPY ../app /workspace/app

ENV PYTHONPATH=/workspace

RUN mkdir -p /workspace/data

USER appuser

CMD ["bash"]
