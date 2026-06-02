from unittest.mock import MagicMock, patch
from app.db.models import Product
from app.main import main

# 【Bランク改善】sys.path.append(...) の重複記述を削除
# (すでに testpy/conftest.py 側で ROOT パスが適切に sys.path に insert されているため動作保証されます)

@patch("app.main.init_db")
@patch("app.main.SessionLocal")
@patch("app.main.fetch_price")
@patch("app.main.save_price_if_changed")
def test_main_integration_flow(mock_save, mock_fetch, mock_session_cls, mock_init_db):
    # ダミーセッションの構築
    mock_session = MagicMock()
    mock_session_cls.return_value = mock_session

    # テスト用ダミー商品の設定
    p1 = Product(id=1, name="Test Item 1", url="http://example.com/1")
    p2 = Product(id=2, name="Test Item 2", url="http://example.com/2")
    mock_session.query.return_value.all.return_value = [p1, p2]

    # モックの戻り値設定（価格）
    mock_fetch.side_effect = [1500, 2800]

    # メインフローの実行
    with patch("argparse.ArgumentParser.parse_args") as mock_args:
        mock_args.return_value = MagicMock(init=False)
        main()

    # 期待される検証
    assert mock_init_db.call_count == 1
    assert mock_fetch.call_count == 2
    assert mock_save.call_count == 2