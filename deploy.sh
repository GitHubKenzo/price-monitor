#!/bin/bash

PROJECT_DIR="/mnt/f/Projects/price-monitor"
SERVER="ubuntu@192.168.3.121"
TARGET_DIR="/opt/price-monitor"

echo "🚀 Starting deployment..."
cd $PROJECT_DIR || exit 1

echo "📤 Uploading project files..."
scp -r \
  main.py \
  utils.py \
  docker-compose.yml \
  Dockerfile \
  products.json \
  scraper/*.py \
  scraper/requirements.txt \
  db/*.py \
  maintenance \
  data \
  $SERVER:$TARGET_DIR


echo "🔄 Restarting Docker Compose on server..."
ssh $SERVER << 'EOF'
cd /opt/price-monitor
/usr/bin/docker compose down
/usr/bin/docker compose up -d --build
EOF

echo "✅ Deployment completed successfully!"
