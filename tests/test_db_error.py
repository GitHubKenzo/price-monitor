from app.db import db
from app.db.models import Base

def test_db_init_error(monkeypatch, capsys):
    # Base.metadata.create_all が例外を投げるようにする
    def raise_error(*args, **kwargs):
        raise Exception("db error")

    monkeypatch.setattr(Base.metadata, "create_all", raise_error)

    try:
        db.init_db()
    except Exception as e:
        # init_db は例外をキャッチしないので、ここで確認する
        assert str(e) == "db error"
