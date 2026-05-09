# Maintenance Tools for Price Monitor

このディレクトリは、**価格監視システムの DB メンテナンス専用ツール**をまとめた領域です。  
本番用コンテナとは責務を分離し、DB の確認・調査・修正を安全に行うための環境を提供します。

---

## 📦 1. 構成
maintenance/
├── Dockerfile
└── docker-compose.yml


- **Dockerfile**  
  - python:3.10-slim ベース  
  - sqlite3 をプリインストール  
  - DB メンテナンス専用の軽量環境

- **docker-compose.yml**  
  - `../data` を `/app/data` にマウント  
  - インタラクティブな bash を起動可能

---

## 🚀 2. 起動方法

### ① maintenance ディレクトリへ移動

cd maintenance


### ② イメージをビルド

docker compose build


### ③ メンテナンス用コンテナを起動（bash が開く）

docker compose run maintenance bash


---

## 🗄 3. SQLite の操作

### DB を開く

sqlite3 /app/data/price.db


### テーブル構造

.schema price_history


### データ確認

SELECT * FROM price_history;


### SQLite の終了

.quit

---

## 🛠 4. よく使うメンテナンス操作

### バックアップ作成

sqlite3 /app/data/price.db ".backup '/app/data/backup.db'"

### 特定商品の履歴を確認

SELECT * FROM price_history WHERE product_id = 1 ORDER BY timestamp DESC;

### データ修正（例：誤った価格を修正）

UPDATE price_history SET price = 9999 WHERE id = 3;

---

## 🔒 5. 本番環境との分離について

- 本番用 scraper コンテナには **sqlite3 を入れない**  
- メンテナンスは **この専用コンテナでのみ実施**  
- これにより  
  - セキュリティ向上  
  - コンテナサイズ削減  
  - CI/CD の安定化  
  - 責務の明確化  
  が実現される

---

## 📝 6. 注意点

- `--rm` によりコンテナは終了時に自動削除される  
- DB ファイルはホスト側の `data/` にあるため安全  
- メンテナンス作業は **本番データを直接扱う**ため慎重に行うこと

---

# ✔ Maintenance README 完成