import json
import os

import requests
from loguru import logger


def serialize(record):
    subset = {
        "timestamp": record["time"].timestamp(),
        "level": record["level"].name,
        "message": record["message"],
        **record["extra"],
    }

    return json.dumps(subset)


def patching(record):
    record["extra"]["serialized"] = serialize(record)


# remove default log handler
logger.remove(0)

# path logger with serialization format
logger = logger.patch(patching)

# add stdout handler
logger.add("/dev/stdout", format="{extra[serialized]}", level="INFO")


def log_response_hook(r: requests.Response, *args, **kwargs) -> None:
    status_code = r.status_code

    content = None
    try:
        content = r.json()
    except requests.exceptions.JSONDecodeError:
        content = ""

    if isinstance(content, dict):
        logger.debug("recieved response from API", status_code=status_code, **content)
    else:
        logger.debug(
            "recieved response from API", status_code=status_code, content=content
        )
