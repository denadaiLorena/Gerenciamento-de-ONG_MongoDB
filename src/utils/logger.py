import logging
import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'app.log')

logger = logging.getLogger('sistema_doacoes')
logger.setLevel(logging.DEBUG)

# File handler
fh = logging.FileHandler(LOG_FILE, encoding='utf-8')
fh.setLevel(logging.DEBUG)

# Console handler (INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(fh)
    logger.addHandler(ch)


def log_exception(exc: Exception, context: str = ''):
    import traceback
    logger.error(f"Exception in [{context}]: {exc}")
    tb = traceback.format_exc()
    logger.debug(tb)


def info(msg: str):
    logger.info(msg)


def debug(msg: str):
    logger.debug(msg)


def error(msg: str):
    logger.error(msg)
