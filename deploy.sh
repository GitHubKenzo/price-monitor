#!/bin/bash

SERVER="ubuntu@192.168.3.121"
TARGET_DIR="/opt/price-monitor"

echo "🚀 Starting deployment..."

# ----------------------------------------

# 1. 必要なディレクトリだけ送る（SSOT）

# ----------------------------------------

echo "📤 Uploading application files..."

scp -r app $SERVER:$TARGET_DIR/
scp -r docker $SERVER:$TARGET_DIR/

# data/ は本番永続化領域なので絶対に上書き禁止

# ----------------------------------------

# 2. 本番サーバで Docker Compose 再起動

# ----------------------------------------

echo "🔄 Restarting Docker Compose on server..."

ssh -t $SERVER << 'EOF'
cd /opt/price-monitor

# 本番側の UID/GID を自動取得

export UID=$(id -u)
export GID=$(id -g)

# data/ は永続化領域なので触らない

docker compose -f docker/docker-compose.yml down --remove-orphans
docker compose -f docker/docker-compose.yml up -d --build

echo "🎉 Deployment finished on server!"
EOF

echo "✅ Deployment completed successfully!"
