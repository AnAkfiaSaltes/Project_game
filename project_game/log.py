# Copyright (c) FlamesCoder. Licensed under the MIT Licence.
# See the LICENCE file in the repository root for full licence text.

import logging
import pathlib
import os


class LoggingFormatter(logging.Formatter):
    black = "\x1b[30m"
    FAIL = "\033[91m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    reset = "\x1b[0m"

    format = "[%(asctime)s] %(levelname)-8s | %(module)-12s | %(message)s"

    FORMATS = {
        logging.DEBUG: gray + format + reset,
        logging.INFO: blue + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: FAIL + format + reset,
    }

    def format(self, record):
        formatter = logging.Formatter(self.FORMATS.get(record.levelno))
        return formatter.format(record)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())

logger.addHandler(console_handler)
