#!/bin/bash

SERVER="ubuntu@192.168.3.121"

echo "🚀 Starting deployment..."

# 1. app ディレクトリを送る
echo "📤 Uploading application files..."
scp -r app $SERVER:/opt/price-monitor/

# 2. docker ディレクトリを送る
echo "📤 Uploading docker files..."
scp -r docker $SERVER:/opt/price-monitor/

# 3. Docker Compose 再起動
echo "🔄 Restarting Docker Compose on server..."
ssh -t $SERVER << 'EOF'
cd /opt/price-monitor
docker compose -f docker/docker-compose.yml down
docker compose -f docker/docker-compose.yml up -d --build
EOF

echo "✅ Deployment completed successfully!"
