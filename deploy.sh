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

# testpy / maintenance / data は送らない
# data は本番永続化領域なので絶対に上書き禁止

# ----------------------------------------
# 2. 本番サーバで Docker Compose 再起動
# ----------------------------------------
echo "🔄 Restarting Docker Compose on server..."

ssh -t $SERVER << 'EOF'
cd /opt/price-monitor

# data/ は永続化領域なので触らない
# app/ と docker/ のみ更新されている

docker compose -f docker/docker-compose.yml down
docker compose -f docker/docker-compose.yml up -d --build

echo "🎉 Deployment finished on server!"
EOF

echo "✅ Deployment completed successfully!"
