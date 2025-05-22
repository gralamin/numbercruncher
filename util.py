import os
import datetime
import logging
import sys

# Requested by Scryfall to rate limit
API_DELAY = 100.0 / 1000.0

logger = logging.getLogger(__name__)


def get_data_file(set_name, meta=False):
    if meta:
        return os.path.join("cache", set_name + ".meta.json")
    return os.path.join("cache", set_name + ".json")


def is_cached(filename):
    cache_time = 6 * 60 * 60  # 60s, 60 min, 6h
    if not os.path.exists(filename):
        logger.debug(f"{filename} is cached - False")
        return False
    info = os.stat(filename)
    modified = datetime.datetime.fromtimestamp(info.st_mtime)
    now = datetime.datetime.now()
    diff = now - modified
    result = diff.total_seconds() <= cache_time
    logger.debug(f"{filename} is cached - {result}")
    return result


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler = logging.FileHandler("crunch.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    stdout_formatter = logging.Formatter("%(message)s")
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.setFormatter(stdout_formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)
