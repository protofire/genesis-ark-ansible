import os
import sys
import requests

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


def log_response_hook(r: requests.Response, *args, **kwargs) -> None:
    status_code = r.status_code
    content = r.json() if r.headers["Content-Type"] == "application/json" else r.content
    if r.status_code != requests.codes.ok:
        logger.error(
            f"recieved error from runner: status_code = '{status_code}', content = '{content}'"
        )
    else:
        logger.debug(
            f"recieved response from runner: status_code = '{r.status_code}', content = '{content}'"
        )
