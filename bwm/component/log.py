import logging
import logging.handlers
import os
import re
from datetime import datetime

from bwm.component.base import Component
from bwm.constants import Env


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

        sqlalchemy_log = logging.getLogger("sqlalchemy")
        sqlalchemy_log.propagate = False
        sqlalchemy_log.addHandler(file_log_handler)

        if self._app.config.get("ENV") == Env.DEV:
            from nplusone.ext.flask_sqlalchemy import NPlusOne

            NPlusOne(self._app)
            self._app.config["NPLUSONE_LOGGER"] = logging.getLogger(
                f"{self._app.name}.nplusone"
            )
            self._app.config["NPLUSONE_LOG_LEVEL"] = logging.ERROR
