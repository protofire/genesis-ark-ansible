import os
import sys

from loguru import logger

logger.add(
    sys.stdout,
    format="{time} {level} {message}",
    filter="cli",
    level="INFO",
)

working_dir = os.getcwd()
logs_dir = os.path.join(working_dir, "logs")
if not os.path.exists(logs_dir):
    os.mkdir(logs_dir)
logs_file = os.path.join(logs_dir, "cli.log")

logger.add(
    logs_file,
    format="{time} {level} {message}",
    level="DEBUG",
)
