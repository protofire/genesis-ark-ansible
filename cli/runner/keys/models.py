import requests
from runner.logging import log_response_hook, logger


class EvmKeysManager:
    def __init__(self, private_key: str, api_url="http://localhost:5000/api/v1"):
        self.api_url = api_url
        self.private_key = private_key

    def get_public_key(self) -> requests.Response:
        params = {"privateKey": self.private_key}
        logger.info(f"get public key: params = '{params}'")
        return self._request(method="POST", path="/keys/public_key", json=params)

    def get_address(self, network_type_for: str) -> requests.Response:
        params = {"networkTypeFor": network_type_for, "privateKey": self.private_key}
        logger.info(f"get wallet address: params = '{params}'")
        return self._request(method="POST", path="/keys/address", json=params)

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
