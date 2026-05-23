#!/bin/bash
set -e

# -----------------------------
# 基本設定
# -----------------------------
SERVER="ubuntu@192.168.3.121"
APP_DIR="/opt/price-monitor/app"
DOCKER_DIR="/opt/price-monitor"

echo "🚀 Starting deployment..."

# -----------------------------
# 本番側の data ディレクトリを保証（DBは破壊しない）
# -----------------------------
echo "📁 Ensuring data directory exists on server..."
ssh $SERVER "mkdir -p /opt/price-monitor/data"

# -----------------------------
# アプリケーションファイルをアップロード（DBは除外）
# -----------------------------
echo "📤 Uploading application source files..."

scp -r \
  main.py \
  utils.py \
  products.json \
  scraper \
  db \
  Dockerfile \
  $SERVER:$APP_DIR/

# -----------------------------
# docker-compose.yml をアップロード
# -----------------------------
echo "📤 Uploading docker-compose.yml..."
scp docker-compose.yml $SERVER:$DOCKER_DIR/

# -----------------------------
# 本番で Docker Compose を再起動
# -----------------------------
echo "🔄 Restarting Docker Compose on server..."
ssh -t $SERVER << 'EOF'
cd /opt/price-monitor
docker compose down
docker compose up -d --build
EOF

echo "✅ Deployment completed successfully!"
