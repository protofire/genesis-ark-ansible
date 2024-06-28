import json
from functools import wraps

import requests
from requests.exceptions import JSONDecodeError

from runner.logging import log_response_hook, logger


def safe(
    exception_raiser,
    default_exception=Exception,
    success_status_code: int = 200,
):
    def safe_outer(fn):
        @wraps(fn)
        def safe_inner(*args, **kwargs):
            res = fn(*args, **kwargs)
            if res.status_code == success_status_code:
                try:
                    return res.json()
                except JSONDecodeError:
                    return res.text
            error = res.json()
            if "error" not in error.keys():
                raise default_exception(error)
            exception_raiser(error)

        return safe_inner

    return safe_outer


class Client:
    LOGGER_NAME = "basic"

    def __init__(self, api_url: str = "http://localhost:5000/api/v1", logger=logger):
        self.api_url = api_url
        self.logger = logger.bind(logger=self.LOGGER_NAME)

    def request(
        self, method: str, path: str, json: dict = {}, params: dict = {}
    ) -> requests.Response:
        """Wraper around the standard request method to apply the logging response hook.

        Args:
            method (str): HTTP method.
            path (str): HTTP path. Will be appended at the end of 'self.api_url'.
            json (dict, optional): JSON payload. Defaults to an empty dict.

        Returns:
            requests.Response: result of the operation
        """
        url = f"{self.api_url}{path}"
        return requests.request(
            method=method,
            url=url,
            json=json,
            params=params,
            hooks={"response": log_response_hook},
        )
