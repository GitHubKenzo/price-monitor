import json
import builtins
from app.utils import load_products_from_json
from app.db.models import Product

class DummyQuery:
    """session.query(Product).filter(...).first() をモックするためのクラス"""
    def __init__(self, exists):
        self.exists = exists

    def filter(self, *args, **kwargs):
        return self

    def first(self):
        return self.exists


class DummySession:
    """SQLAlchemy Session の add / commit / query をモック"""
    def __init__(self, exists=False):
        self.add_called = False
        self.commit_called = False
        self.added_product = None
        self.exists = exists

    def query(self, model):
        return DummyQuery(self.exists)

    def add(self, product):
        self.add_called = True
        self.added_product = product

    def commit(self):
        self.commit_called = True


def test_load_products_from_json_adds_new_product(tmp_path, capsys):
    # テスト用 JSON ファイルを作成
    json_path = tmp_path / "products.json"
    data = [{"name": "Test Product", "url": "http://example.com"}]
    json_path.write_text(json.dumps(data), encoding="utf-8")

    # DB に存在しないケース（exists=False）
    session = DummySession(exists=False)

    load_products_from_json(session, path=str(json_path))

    # add と commit が呼ばれている
    assert session.add_called
    assert session.commit_called

    # 追加された Product の内容確認
    assert session.added_product.name == "Test Product"
    assert session.added_product.url == "http://example.com"

    # print ログ確認
    captured = capsys.readouterr()
    assert "[INFO] Added product: Test Product" in captured.out


def test_load_products_from_json_skip_existing(tmp_path, capsys):
    # テスト用 JSON ファイルを作成
    json_path = tmp_path / "products.json"
    data = [{"name": "Existing Product", "url": "http://example.com"}]
    json_path.write_text(json.dumps(data), encoding="utf-8")

    # DB にすでに存在するケース（exists=True）
    session = DummySession(exists=True)

    load_products_from_json(session, path=str(json_path))

    # add も commit も呼ばれない
    assert not session.add_called
    assert not session.commit_called

    # print ログも出ない
    captured = capsys.readouterr()
    assert captured.out == ""
