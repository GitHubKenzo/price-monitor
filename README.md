# Yahooショッピング価格監視システム  
Yahooショッピングの商品価格を自動で取得し、価格変動を検知して記録するシステムです。  
Docker により環境差異を排除し、どの環境でも同じ動作を再現できます。

---

## 🚀 特徴（発注者向けアピールポイント）

### ✔ Yahooショッピングの HTML 構造に完全対応（A‑1：堅牢な価格抽出ロジック）
Yahooショッピングは商品ページごとに HTML 構造が異なります。  
本システムでは **構造化データ（meta[itemprop="price"]）を最優先**し、  
さらに複数の CSS セレクタを組み合わせた価格抽出ロジックを実装しています。

価格抽出の優先順位：

1. `<meta itemprop="price">`  
2. `itemprop="price"`  
3. 汎用クラス（`.elPrice`, `.price`, `.Value` など）

これにより、**ポイント数や割引率の誤取得を完全排除**し、  
Yahooショッピングのテンプレート差異にも強い安定したスクレイピングを実現しています。

---

### ✔ 価格取得の安定性を最大化（複数セレクタ対応）
商品ページごとの HTML 差異に対応するため、複数の候補セレクタを自動判定します。

- meta[itemprop="price"]  
- itemprop="price"  
- `.elPrice` / `.elPriceNumber` / `.elPriceValue`  
- `.elPrice__value`  
- その他、商品固有の構造にも対応可能  

**UI 変更やテンプレート差異にも強い設計**になっています。

---

### ✔ JSON による商品リスト管理（C‑1：init モード）
`products.json` に商品を記述し、以下で DB に初期登録できます：

```
python3 main.py --init
```

開発・本番どちらでも同じ商品リストを扱えるため、  
**運用の一貫性が高い**設計です。

---

### ✔ 価格変動時のみ記録（差分保存）
前回価格と比較し、**変動があった場合のみ DB に保存**します。  
無駄なデータ増加を防ぎ、履歴が見やすくなります。

---

### ✔ Docker による完全再現性（開発・本番共通）
本システムは Docker Compose で構成されており、以下を含みます：

- Python スクレイパーコンテナ  
- SQLite データベース（軽量・高速）  
- メンテナンス用コンテナ（DB 確認用）  

**WSL2 → Hyper‑V 本番サーバー** へのデプロイも  
`deploy.sh` により完全自動化されています。

---

### ✔ cron による完全自動運用（本番）
Hyper‑V 上の Ubuntu Server では、cron が毎時 00 分に scraper を実行します：

```
0 * * * * cd /opt/price-monitor && /usr/libexec/docker/cli-plugins/docker-compose run --rm scraper
```

これにより、**24 時間自動で価格監視が継続**されます。

---

### ✔ 通知機能は安全にダミー化（B‑2）
本番環境では通知機能をダミー化しており、  
外部 API の障害やトークン切れで処理が止まることはありません。

（必要に応じて Slack / LINE Notify / Gmail などに切り替え可能）

---

## 📁 ディレクトリ構造

```
price-monitor/
├── scraper/
│   ├── scraper.py         # Yahooショッピング対応スクレイパー（A‑1 ロジック）
│   ├── models.py          # DB モデル
│   ├── logic.py           # 価格比較・保存ロジック
│   ├── db.py              # SQLite とのやり取り
│   └── requirements.txt   # Python依存パッケージ
├── data/
│   └── price.db           # SQLite データベース
├── products.json          # 商品リスト（init モードで読み込み）
├── utils.py               # 通知（本番はダミー）
├── main.py                # 実行フロー（--init 対応）
├── Dockerfile
├── docker-compose.yml
└── deploy.sh              # 本番デプロイ自動化
```

---

## 🔧 技術スタック

- **Python 3.x**
- **BeautifulSoup4 / lxml**
- **SQLite**
- **Docker / Docker Compose**
- **cron（本番自動実行）**
- **Hyper‑V Ubuntu Server（本番環境）**

---

## 🧩 処理フロー

1. DB に登録された商品URLを取得  
2. HTML を取得（requests）  
3. 構造化データ → CSS セレクタの順で価格を抽出  
4. 前回価格と比較  
5. 変動があれば記録（通知はダミー）  
6. 新しい価格を DB に保存  

---

## 🛠 今後の拡張性

- Amazon / 楽天市場への対応  
- 価格推移グラフの自動生成（Dash / Streamlit）  
- Discord / Slack 通知  
- 商品の自動追加 API  

---

## 📩 お問い合わせ
本システムの導入・カスタマイズ・追加機能開発など、  
お気軽にご相談ください。
