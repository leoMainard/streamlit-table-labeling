import os
import sys
import logging
from enum import Enum

class Environnement:
    _configuration = None

    @classmethod
    def _load_config(cls):
        if cls._configuration is None:
            cls._configuration = {
                "DB_NAME": os.getenv("DB_NAME"),
                "DB_HOSTNAME": os.getenv("DB_HOSTNAME"),
                "DB_PORT": os.getenv("DB_PORT"),
                "DB_USER": os.getenv("DB_USER"),
                "DB_PASSWORD": os.getenv("DB_PASSWORD"),
            }
    @classmethod
    def config(cls, name):
        cls._load_config()
        try:
            return cls._configuration[name]
        except KeyError:
            raise KeyError(f"Configuration '{name}' not found.")


class Vars(Enum):

    TABLE_LABELS = "DAB,VAM,SIN,AUTRE"


# ---------- LOGGER SETUP WITH COLORS ----------

class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.INFO: "\033[92m",    # Green
        logging.WARNING: "\033[93m", # Yellow
        logging.ERROR: "\033[91m",   # Red
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelno, "")
        message = super().format(record)
        return f"{color}{message}{self.RESET}"

# Create the logger
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)  # You can adjust the level here

# Create console handler
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)

# Set formatter
formatter = ColorFormatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
ch.setFormatter(formatter)

# Avoid adding multiple handlers if already added
if not logger.handlers:
    logger.addHandler(ch)