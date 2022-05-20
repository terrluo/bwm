import logging
import os
import re
from datetime import datetime

from bwm.registercomponent.base import Component


class NoEscape(logging.Filter):
    def __init__(self):
        self.regex = re.compile(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]")

    def strip_esc(self, s):
        try:  # string-like
            return self.regex.sub("", s)
        except Exception:  # non-string-like
            return s

    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = self.strip_esc(record.msg)
        if type(record.args) is tuple:
            record.args = tuple(map(self.strip_esc, record.args))
        return True


class LogComponent(Component):
    def register(self):
        level = os.getenv("BWM_LOG_LEVEL", "INFO").upper()
        log_name = datetime.now().strftime("%Y%m%d%H")

        logging.basicConfig(level=level)
        file_log_handler = logging.handlers.RotatingFileHandler(
            f"logs/{log_name}.log", maxBytes=1024 * 1024 * 10, backupCount=100
        )
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s"
        )
        file_log_handler.setFormatter(formatter)
        file_log_handler.addFilter(NoEscape())
        logger = logging.getLogger()
        logger.addHandler(file_log_handler)
