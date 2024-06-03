import requests
from runner.logging import log_response_hook


class Client:
    def __init__(self, api_url: str = "http://localhost:5000/api/v1"):
        self.api_url = api_url

    def request(self, method: str, path: str, json: dict = {}) -> requests.Response:
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
