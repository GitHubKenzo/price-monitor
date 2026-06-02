import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base

DB_PATH = os.getenv("DB_PATH", "/workspace/data/price.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    Base.metadata.create_all(bind=engine)