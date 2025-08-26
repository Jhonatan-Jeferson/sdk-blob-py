import logging


class Formatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_format = "%(asctime)s - %(name)s -"
        formats : dict[str, str] = {
            "DEBUG": "\033[36m",
            "INFO": "\033[34m",
            "WARNING": "\033[33m",
            "ERROR": "\033[31m",
            "CRITICAL": "\033[31;1m"
        }
        log_format += formats.get(record.levelname, "") + " [%(levelname)s] - %(message)s\033[0m"
        self._style._fmt = log_format
        return super().format(record)
    

logger = logging.getLogger("SquareCloud")
logger.setLevel(logging.NOTSET)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(Formatter(datefmt="%Y-%m-%d %H:%M:%S"))
logger.addHandler(stream_handler)