import logging
import functools
import sys
try:
    from colorama import init as colorama_init
    colorama_init()
except Exception:
    pass

class ColorFormatter(logging.Formatter):
    RESET = "\033[0m"
    COLORS = {
        logging.DEBUG: "\033[36m",
        logging.INFO: "\033[32m",
        logging.WARNING: "\033[33m",
        logging.ERROR: "\033[31m",
        logging.CRITICAL: "\033[1;31m"
    }
    def __init__(self, fmt=None, datefmt=None, use_color=None):
        super().__init__(fmt, datefmt)
        # color only when writing to a TTY
        self.use_color = sys.stderr.isatty() if use_color is None else use_color

    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)
        if self.use_color:
            color = self.COLORS.get(record.levelno, "")
            if color:
                return f"{color}{msg}{self.RESET}"
        return msg

def setup_custom_logger(name:str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set the minimum logging level

    # Create a console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)  # Set the level for this handler

    # Create a formatter and add it to the handler
    formatter = ColorFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', use_color=True)
    ch.setFormatter(formatter)

    if not logger.handlers:  # Prevent adding multiple handlers if run multiple times
        logger.addHandler(ch)
    return logger