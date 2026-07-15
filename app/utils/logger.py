import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

log_file = LOG_DIR / "system-health.log"

formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

file_handler = RotatingFileHandler(
    filename=log_file,
    maxBytes=1024 * 1024, # 1MB
    backupCount=10
)

file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger = logging.getLogger("system-health-api")

logger.setLevel(logging.INFO)

logger.addHandler(file_handler)
logger.addHandler(console_handler)