import logging
from logging.handlers import RotatingFileHandler
import os

# SQLAlchemy のログを抑制
logging.getLogger("sqlalchemy").setLevel(logging.WARNING)

LOG_DIR = "/workspace/logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

# 独立したロガー
logger = logging.getLogger("price_monitor")
logger.setLevel(logging.INFO)

# root logger に伝播しない（最重要）
logger.propagate = False

if not logger.handlers:
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    ))

    logger.addHandler(file_handler)
