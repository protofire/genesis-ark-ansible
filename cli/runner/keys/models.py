import requests
from runner.logging import logger
from runner.client import Client


class KeysClient(Client):
    def get_public_key(self, private_key: str) -> requests.Response:
        params = {"privateKey": private_key}
        logger.info(f"get public key: params = '{params}'")
        return self.request(method="POST", path="/keys/public_key", json=params)

    def get_address(self, private_key: str, network_type_for: str) -> requests.Response:
        params = {"networkTypeFor": network_type_for, "privateKey": private_key}
        logger.info(f"get wallet address: params = '{params}'")
        return self.request(method="POST", path="/keys/address", json=params)
