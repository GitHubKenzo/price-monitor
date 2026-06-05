# Yahooショッピング価格監視システム

Yahooショッピングの商品価格を定期監視し、
価格変動を検知して履歴保存および通知を行うシステムです。

Docker を利用して開発環境と本番環境の差異を排除し、
Hyper-V Ubuntu 上で安定稼働することを目的としています。

---

## 🚀 主な機能

### ✔ Yahooショッピング価格取得

商品ページから価格を取得します。

以下の優先順位で価格を抽出します。

1. JSON-LD（offers.price）
2. JSON-LD（offers.lowPrice）
3. meta[itemprop="price"]
4. itemprop="price"
5. 汎用価格クラス検索

関連商品価格やポイント数などの誤取得を防止するロジックを実装しています。

---

### ✔ 価格変動監視

前回取得価格と比較し、
価格変動が発生した場合のみ履歴へ保存します。

保存先：

- SQLite
- price_history テーブル

---

### ✔ 通知機能

価格変動検知時に通知を送信します。

通知処理は notifier モジュールとして独立しており、
将来的な通知先追加にも対応しやすい構成です。

---

### ✔ 通信リトライ

一時的な通信エラー発生時は再試行します。

- requests例外対応
- HTTPエラー対応
- 一定時間待機後リトライ

---

## 🧪 品質保証

pytest による自動テストを実施しています。

現在の結果：

- 29 Tests Passed
- Coverage 100%

対象：

- スクレイパー
- DB保存処理
- 通知処理
- メイン処理
- リトライ処理
- 初期化処理
- エラー処理

---

## 📁 Git管理構成

```text
price-monitor/
├── app/
│   ├── db/
│   ├── scraper/
│   ├── main.py
│   └── utils.py
├── tests/
├── docker/
├── data/
├── deploy.sh
├── requirements.txt
├── requirements-prod.txt
├── products.json
└── README.md
```

---

## 🖥 本番配置構成

```text
/opt/price-monitor/
├── app/
├── docker/
├── data/
├── logs/
└── app/.env
```

---

## ⚙️ 開発環境セットアップ

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

---

## ⚙️ テスト実行

### ローカル

```bash
pytest -x -v
```

### Docker

```bash
docker compose -f docker/docker-compose.test.yml up --abort-on-container-exit
```

---

## 🚀 デプロイ

deploy.sh を実行します。

```bash
./deploy.sh
```

deploy.sh は以下を実施します。

1. pytest実行
2. app/同期
3. docker/同期
4. 本番Docker再ビルド
5. 本番Docker再起動

---

## 🔧 使用技術

- Python 3.10
- BeautifulSoup4
- lxml
- SQLAlchemy
- SQLite
- requests
- pytest
- Docker
- Docker Compose

---

## 📝 更新履歴

### 2026-06-05

- JSON-LD価格抽出対応
- lowPrice対応
- 関連商品価格誤取得防止
- テスト29件整備
- Coverage 100%達成
- Dockerテスト環境整備
- deploy.sh改善