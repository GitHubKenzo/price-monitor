import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest.mock import MagicMock, patch
from app.main import main
from app.db.models import Product


def test_main_init_mode(monkeypatch, caplog):
    monkeypatch.setattr("sys.argv", ["main.py", "--init"])

    # ★ DB 初期化を無効化
    monkeypatch.setattr("app.main.init_db", lambda: None)

    mock_session = MagicMock()
    monkeypatch.setattr("app.main.SessionLocal", lambda: mock_session)

    
    # argparse の --init を強制
    monkeypatch.setattr("sys.argv", ["main.py", "--init"])

    # SessionLocal をモック
    mock_session = MagicMock()
    monkeypatch.setattr("app.main.SessionLocal", lambda: mock_session)

    # load_products_from_json をモック
    mock_load = MagicMock()
    monkeypatch.setattr("app.main.load_products_from_json", mock_load)

    # Product のリストを返すようにする
    mock_product = Product(id=1, name="商品A", url="http://example.com")
    mock_session.query().all.return_value = [mock_product]

    # fetch_price をモック
    mock_fetch = MagicMock(return_value=1000)
    monkeypatch.setattr("app.main.fetch_price", mock_fetch)

    # save_price_if_changed をモック
    mock_save = MagicMock()
    monkeypatch.setattr("app.main.save_price_if_changed", mock_save)

    with caplog.at_level("INFO"):
        main()

    # --init のときは JSON 取り込みが呼ばれる
    mock_load.assert_called_once()

    # fetch_price → save_price_if_changed の流れが呼ばれる
    mock_fetch.assert_called_once_with("http://example.com")
    mock_save.assert_called_once()


def test_main_normal_mode(monkeypatch, caplog):
    monkeypatch.setattr("sys.argv", ["main.py"])

    # ★ DB 初期化を無効化（これが抜けていた）
    monkeypatch.setattr("app.main.init_db", lambda: None)

    mock_session = MagicMock()
    monkeypatch.setattr("app.main.SessionLocal", lambda: mock_session)

    mock_load = MagicMock()
    monkeypatch.setattr("app.main.load_products_from_json", mock_load)

    mock_product = Product(id=1, name="商品A", url="http://example.com")
    mock_session.query().all.return_value = [mock_product]

    mock_fetch = MagicMock(return_value=1000)
    monkeypatch.setattr("app.main.fetch_price", mock_fetch)

    mock_save = MagicMock()
    monkeypatch.setattr("app.main.save_price_if_changed", mock_save)

    with caplog.at_level("INFO"):
        main()

    mock_load.assert_not_called()
    mock_fetch.assert_called_once()
    mock_save.assert_called_once()