import logging
from logging.handlers import RotatingFileHandler

from app.utils.logger import logger

def test_logger_name():
    assert logger.name == "system-health-api"


def test_logger_level():
    assert logger.level == logging.INFO


def test_logger_has_rotating_file_handler():
    assert any(
        isinstance(handler, RotatingFileHandler)
        for handler in logger.handlers
    )


def test_logger_has_stream_handler():
    assert any(
        isinstance(handler, logging.StreamHandler)
        for handler in logger.handlers
    )
    

def test_logger_can_log_message(caplog):

    with caplog.at_level(
        logging.INFO,
        logger="system-health-api"
    ):
        logger.info("Unit Test Log")

    assert "Unit Test Log" in caplog.text