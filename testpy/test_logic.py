import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest.mock import MagicMock
from app.db.logic import save_price_if_changed
from app.db.models import PriceHistory

from unittest.mock import MagicMock
from app.db.logic import save_price_if_changed
from app.db.models import PriceHistory
def test_save_price_first_time():
    # モック session
    session = MagicMock()

    # last = None を返すように設定
    session.query().filter().order_by().first.return_value = None

    # モック product
    product = MagicMock()
    product.id = 1
    product.name = "テスト商品"

    save_price_if_changed(session, product, 1000)

    # INSERT（add）が呼ばれたか？
    assert session.add.called
    # commit が呼ばれたか？
    assert session.commit.called

    # add に渡された PriceHistory の中身を確認
    history_obj = session.add.call_args[0][0]
    assert isinstance(history_obj, PriceHistory)
    assert history_obj.product_id == 1
    assert history_obj.price == 1000
def test_save_price_changed():
    session = MagicMock()

    # last.price = 900 → new_price = 1000
    last = MagicMock()
    last.price = 900
    session.query().filter().order_by().first.return_value = last

    product = MagicMock()
    product.id = 1
    product.name = "テスト商品"

    save_price_if_changed(session, product, 1000)

    assert session.add.called
    assert session.commit.called

    history_obj = session.add.call_args[0][0]
    assert history_obj.price == 1000
def test_save_price_no_change():
    session = MagicMock()

    # last.price = 1000 → new_price = 1000
    last = MagicMock()
    last.price = 1000
    session.query().filter().order_by().first.return_value = last

    product = MagicMock()
    product.id = 1
    product.name = "テスト商品"

    save_price_if_changed(session, product, 1000)

    # add も commit も呼ばれない
    session.add.assert_not_called()
    session.commit.assert_not_called()
def test_save_price_changed_log(caplog):
    session = MagicMock()

    last = MagicMock()
    last.price = 900
    session.query().filter().order_by().first.return_value = last

    product = MagicMock()
    product.id = 1
    product.name = "テスト商品"

    with caplog.at_level("INFO"):
        save_price_if_changed(session, product, 1000)

    assert "Price changed! テスト商品: 1000 円" in caplog.text
def test_save_price_no_change_log(caplog):
    session = MagicMock()

    last = MagicMock()
    last.price = 1000
    session.query().filter().order_by().first.return_value = last

    product = MagicMock()
    product.id = 1
    product.name = "テスト商品"

    with caplog.at_level("INFO"):
        save_price_if_changed(session, product, 1000)

    assert "No change: テスト商品 は前回と同じ価格 1000 円" in caplog.text
