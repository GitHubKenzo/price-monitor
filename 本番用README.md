# price-monitor 本番環境構築手順（Hyper‑V + Ubuntu Server 22.04）

このドキュメントは、Windows 上の Hyper‑V に Ubuntu Server 22.04 LTS を構築し、  
Docker + cron による Yahoo 商品価格モニタリングツール（price-monitor）を  
本番運用するための手順をまとめたものです。

---

## 1. Hyper‑V の有効化

1. Windows 検索窓に「Windows の機能の有効化または無効化」と入力して開きます。
2. **Hyper‑V** にチェックを入れます。  
   - Hyper‑V プラットフォーム  
   - Hyper‑V 管理ツール  
3. 画面の指示に従って PC を再起動します。

---

## 2. Hyper‑V 仮想スイッチの作成

外部ネットワーク（インターネット）と通信できるように、仮想スイッチを設定します。

1. Hyper‑V マネージャーを開き、右側の操作パネルから「仮想スイッチ マネージャー」を選択します。
2. 「新しい仮想ネットワーク スイッチ」で **外部** を選択し、「仮想スイッチの作成」をクリックします。
3. 以下の通り設定情報を入力します：
   - 名前：`ExternalSwitch`
   - 接続の種類：外部ネットワーク（現在インターネットに使用している物理 NIC を選択）
4. 「適用」をクリックし、警告が表示された場合は「はい」を選択して適用します。

---

## 3. Ubuntu Server 22.04 LTS の ISO ダウンロード

1. Ubuntu 公式サイトのダウンロードページにアクセスします。
2. 「Ubuntu Server 22.04.x LTS」の ISO イメージファイルをダウンロードします。
3. ダウンロードした ISO ファイルは、ローカルの分かりやすい場所（例：`C:\ISO\`）に保存しておきます。

---

## 4. 仮想マシンの作成と設定

1. Hyper‑V マネージャーの「新規」 → 「仮想マシン」を選択します。
2. ウィザードに従って以下の通り設定を進めます：
   - **名前**: `price-monitor-prod`
   - **世代**: `第 2 世代`（※推奨）
   - **起動メモリ**: `4096MB`（動的メモリを有効にする）
   - **ネットワークの構成**: 接続に先ほど作成した `ExternalSwitch` を選択
   - **仮想ハード ディスク**: 「仮想ハード ディスクを作成する」を選択し、サイズを `50GB` に指定
   - **インストール オプション**: 「ブートイメージ ファイルからオペレーティング システムをインストールする」を選び、手順3でダウンロードした Ubuntu の ISO ファイルを指定
3. 作成完了後、仮想マシンの「設定」を開き、「セキュリティ」項目にある **「セキュア ブートを有効にする」のチェックを外す** か、テンプレートを `Microsoft UEFI 証明書機関` に変更します（Ubuntu を正常に起動させるため）。

---

## 5. Ubuntu Server のインストール手順

1. 仮想マシンを「接続」し、「起動」します。
2. インストーラーが起動したら、以下の通りセットアップを進めます：
   - **Language**: `English`（サーバー運用の標準）
   - **Keyboard**: Layout を `Japanese`、Variant を `Japanese (OADG 109A)` に設定
   - **Type of installation**: `Ubuntu Server`（デフォルト）
   - **Network connections**: DHCP により自動的に IP アドレスが割り当てられていることを確認
   - **Storage configuration**: `Use an entire disk` にチェックを入れ、デフォルトのまま進める
   - **Profile setup**: 
     - Your name: `ubuntu`
     - Your server's name: `price-monitor-prod`
     - Pick a username: `ubuntu`
     - Choose a password: （任意の強力なパスワードを入力）
   - **SSH Setup**: `Install OpenSSH server` に必ず **チェック（[X]）** を入れる
   - **Featured Server Snaps**: 何も選択せず `Done` を選択
3. インストール完了後、`Reboot Now` を選択します。「Please remove the installation medium...」と表示された場合は、Enter キーを押します。

---

## 6. パッケージの初期アップデート

OS 起動後、SSH または Hyper‑V コンソールからログインし、システムを最新化します。

```bash
sudo apt update
sudo apt upgrade -y
```

カーネルの更新等が適用される場合があるため、一度再起動を行います：

```bash
sudo reboot
```
## 7. Docker / Docker Compose のインストール

1. Ubuntu に Docker および Docker Compose をインストールします。
   bash 0092	   sudo apt install docker.io docker-compose -y 0093	   
2. インストール完了後、Docker サービスが正常にアクティブになっているか確認します。
   bash 0096	   systemctl status docker 0097	   

---

## 8. sudo なしでの Docker コマンド実行設定

1. セキュリティ上、一般ユーザー（ubuntu）で sudo を付与せずに docker コマンドを実行できるようにユーザーグループへ追加します。
   bash 0105	   sudo usermod -aG docker $USER 0106	   
2. 反映させるため、一度SSH接続をログアウトするか、以下のコマンドを実行してグループ設定を即時適用します。
   bash 0109	   newgrp docker 0110	   
3. テスト用のコマンドを実行し、エラーなしで実行できることを確認します。
   bash 0113	   docker ps 0114	   

---

## 9. 本番アプリ配置ディレクトリの作成

1. 開発マシンからデプロイされたアプリケーションコードを配置するための、本番用ルートディレクトリを作成します。
   bash 0122	   sudo mkdir -p /opt/price-monitor 0123	   sudo chown ubuntu:ubuntu /opt/price-monitor 0124	   

---

## 10. アプリケーションのデプロイと初期設定

1. 開発環境のルートにあるデプロイスクリプト（deploy.sh）を実行するか、GitHub Actions のワークフローを動かしてファイルをサーバーへコピーします。
2. サーバー側（/opt/price-monitor）に以下のファイル群が配置されていることを確認します。
   bash 0133	   ls -la /opt/price-monitor 0134	   
3. 価格監視で用いる LINE Notify 用の環境変数を定義するため、ホスト（Ubuntu）側のルートディレクトリ配下に環境設定用の .env ファイルを作成します。
   bash 0137	   echo "LINE_NOTIFY_TOKEN=YOUR_REAL_LINE_NOTIFY_TOKEN" > /opt/price-monitor/.env 0138	   

---

## 11. cron（定期自動実行）の設定

Yahooショッピングの価格変更を自動的に検知・追跡するため、ホスト側の cron を利用してタスクを定時スケジューリングします。コンテナ実行時に --rm フラグを設定することで、終了後に不要となった使い捨てスクレイパーコンテナを安全に自動クリーンアップします。

1. ホスト環境の cron 設定画面を開きます。
   bash 0148	   crontab -e 0149	   
2. 初めて開く場合はテキストエディタの選択を求められるので、標準的な nano（通常は 1）を選びます。
   text 0152	   Select an editor.  To change later, run 'select-editor'. 0153	     1. /bin/nano        <---- easiest 0154	     2. /usr/bin/vim.basic 0155	     3. /usr/bin/vim.tiny 0156	   
3. ファイルの最下行に、以下のスケジュール実行記述を追加します。
   - 例1：毎時0分（1時間に1回）に実行する場合
     text 0160	     0 * * * * cd /opt/price-monitor && /usr/bin/docker compose run --rm scraper 0161	     
   - 例2：毎日 朝9:00 と 夜21:00 の2回に分けてチェックする場合
     text 0164	     0 9,21 * * * cd /opt/price-monitor && /usr/bin/docker compose run --rm scraper 0165	     
4. 編集が終わったら、Ctrl+O → Enter で保存し、Ctrl+X で終了します。

---

## 12. 本番用ボリュームの永続化と保守について

- SQLite DBファイル（price.db）は、ホスト側の /opt/price-monitor/data ディレクトリにボリュームマウント（./data:/app/data）経由で保存されます。
- コードやコンテナイメージのバージョンアップを行うために docker compose down やイメージのビルド再起動を行っても、価格監視の過去ログや登録済み商品は一切消えず、安全に保存・継承されます。
- 定期的なバックアップを取得したい場合は、ホスト側の /opt/price-monitor/data/price.db をコピー・退避させるだけで瞬時に復元ポイントを作成することができます。