# Yahooショッピング価格監視システム  
Yahooショッピングの商品価格を自動で取得し、価格変動を検知した際に LINE 通知を送るシステムです。  
Docker により環境差異を排除し、どの環境でも同じ動作を再現できます。

---

## 🚀 特徴（発注者向けアピールポイント）

### ✔ Yahooショッピングの HTML 構造に完全対応
Yahooショッピングは商品ページごとに HTML 構造が微妙に異なります。  
本システムでは **複数の CSS セレクタを組み合わせた価格抽出ロジック**を実装し、  
テンプレート差異に強い安定したスクレイピングを実現しています。

### ✔ 価格取得の安定性を最大化（複数セレクタ対応）
以下のような複数パターンを自動判定し、最初に取得できた価格を採用します：

- `.elPrice`
- `.elPriceNumber`
- `.elPriceValue`
- `.elPrice__value`
- その他、商品固有の構造にも対応可能

これにより、**商品ごとの HTML 差異や UI 変更にも強い**設計になっています。

### ✔ JavaScript 依存ページにも対応（Selenium）
一部の商品ページは JavaScript により価格が描画されます。  
その場合は **Selenium（ヘッドレス Chrome）** を自動的に使用し、  
静的 HTML では取得できない価格も確実に取得できます。

### ✔ 価格変動時に LINE 通知
価格が前回より下がった場合、LINE Notify API を使って即時通知します。

通知内容例：

- 商品名
- 現在価格
- 前回価格
- 商品URL

これにより、**値下げタイミングを逃さず購入判断が可能**になります。

### ✔ Docker による完全再現性
本システムは Docker Compose で構成されており、以下を含みます：

- Python スクレイパーコンテナ
- PostgreSQL データベース
- 必要ライブラリを固定した requirements.txt

開発環境・本番環境の差異を排除し、  
**どの環境でも同じ動作を保証**します。

---

## 📁 ディレクトリ構造

price-monitor/
├── scraper/
│   ├── main.py            # 全体の実行フロー
│   ├── scraper.py         # Yahooショッピング対応スクレイパー
│   ├── parser.py          # HTML解析・価格抽出ロジック
│   ├── db.py              # PostgreSQL とのやり取り
│   ├── notifier.py        # LINE通知
│   └── requirements.txt   # Python依存パッケージ
├── docker-compose.yml      # Docker構成
└── README.md               # 本ドキュメント


---

## 🔧 技術スタック

- **Python 3.x**
- **BeautifulSoup4 / lxml**
- **Selenium（ヘッドレス Chrome）**
- **PostgreSQL**
- **Docker / Docker Compose**
- **LINE Notify API**

---

## 🧩 処理フロー

1. DB に登録された商品URLを取得  
2. HTML を取得（静的 or Selenium）  
3. 複数 CSS セレクタで価格を抽出  
4. 前回価格と比較  
5. 変動があれば LINE 通知  
6. 新しい価格を DB に保存  

---

## 🛠 今後の拡張性

- Amazon / 楽天市場への対応  
- 価格推移グラフの自動生成  
- Discord / Slack 通知  
- 商品の自動追加 API  

---

## 📩 お問い合わせ
本システムの導入・カスタマイズ・追加機能開発など、  
お気軽にご相談ください。
