import logging
from utils.logger_factory import get_logger

def test_logger_logs_message(caplog):
    logger = get_logger(__name__)
    with caplog.at_level(logging.INFO):
        logger.info("This is a test log")
    assert "This is a test log" in caplog.text


def test_logger_logs_at_different_levels(caplog):
    logger = get_logger(__name__)
    with caplog.at_level(logging.WARNING):
        logger.debug("This should not appear")
        logger.info("This should not appear")
        logger.warning("This is a warning")
        logger.error("This is an error")

    log_messages = caplog.text
    assert "This is a warning" in log_messages
    assert "This is an error" in log_messages
    assert "This should not appear" not in log_messages
