# price-monitor 本番環境構築手順（Hyper‑V + Ubuntu Server 22.04）

このドキュメントは、Windows 上の Hyper‑V に Ubuntu Server 22.04 LTS を構築し、  
Docker + cron による Yahoo 商品価格モニタリングツール（price-monitor）を  
本番運用するための手順をまとめたものです。

---

# 1. Hyper‑V の有効化

1. Windows 検索 → 「Windows の機能の有効化または無効化」
2. **Hyper‑V** にチェック  
   - Hyper‑V プラットフォーム  
   - Hyper‑V 管理ツール  
3. 再起動

---

# 2. Hyper‑V 仮想スイッチの作成

1. Hyper‑V マネージャー → 「仮想スイッチ マネージャー」
2. 新規作成 → **外部**
3. 接続先：物理 NIC
4. 名前例：`ExternalSwitch`

---

# 3. Ubuntu Server 22.04 LTS の ISO をダウンロード

- Ubuntu 22.04.5 LTS を公式サイトから取得  
- ISO を任意の場所に保存

---

# 4. 仮想マシンの作成

| 項目 | 設定 |
|------|------|
| 名前 | price-monitor-prod |
| 世代 | 第2世代 |
| メモリ | 4096MB（動的メモリ ON） |
| CPU | 2〜4 コア |
| ネットワーク | ExternalSwitch |
| HDD | 50GB（VHDX） |

---

# 5. Ubuntu Server のインストール

1. 言語：English  
2. キーボード：Japanese（OADG 109A）  
3. Install Ubuntu Server  
4. ネットワーク：DHCP のまま  
5. Guided – use entire disk  
6. ユーザー：`ubuntu`  
7. ホスト名：`price-monitor-prod`  
8. OpenSSH：YES  

---

# 6 初期セットアップ

```bash
sudo apt update
sudo apt upgrade -y
```

必要なら再起動：

```bash
sudo reboot
```
---

# 7 Docker / Docker Compose のインストール

```bash
sudo apt install docker.io docker-compose -y
```

Docker の状態確認：

```bash
systemctl status docker
```
---

# 8 Docker を sudo なしで使えるようにする

```bash
sudo usermod -aG docker $USER
```

※ 一度ログアウト → ログインが必要。

# 9 本番アプリ配置ディレクトリの作成

```bash
sudo mkdir -p /opt/price-monitor
sudo chown ubuntu:ubuntu /opt/price-monitor
```

---

# 10 Docker 動作確認

```bash
docker ps
```

エラーが出なければ OK。
---

# 11 本番環境の目的（補足）

この環境は、Yahoo 商品価格モニタリングツール（price-monitor）を
Docker + cron で安定稼働させるための疑似本番環境です。

Hyper‑V 上で Ubuntu Server 22.04 LTS を稼働

Docker コンテナでアプリケーションを運用

/opt/price-monitor に本番コードを配置

volume による DB 永続化

cron + logrotate による定期実行とログ管理

GitHub Actions による自動デプロイ（後述）