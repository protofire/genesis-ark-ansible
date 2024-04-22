import requests
from runner.logging import logger


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


class JobManager:
    def __init__(self, job_id: str):
        self.job_id

    def _request(self, method: str, path: str, json: dict = {}) -> requests.Response:
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
            hooks={"response": log_response_hook},
        )
