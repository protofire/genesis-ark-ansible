from runner.client import Client, safe
from runner.keys.exceptions import (
    KeysClientException,
    NetworkNotConnectedException,
    NetworkNotFoundException,
)
from runner.logging import logger


def exception_raiser(error_description: str, error_message: str) -> None:
    match error_description:
        case "network_not_connected":
            raise NetworkNotConnectedException(error_message)
        case "network_not_found":
            raise NetworkNotFoundException(error_message)
        case _:
            raise KeysClientException(error_message)


class KeysClient(Client):
    @safe(exception_raiser=exception_raiser, default_exception=KeysClientException)
    def get_public_key(self, private_key: str) -> dict:
        params = {"privateKey": private_key}
        logger.info(f"get public key: params = '{params}'")
        return self.request(method="POST", path="/keys/public_key", json=params)

    @safe(exception_raiser=exception_raiser, default_exception=KeysClientException)
    def get_address(self, private_key: str, network_type_for: str) -> dict:
        params = {"networkTypeFor": network_type_for, "privateKey": private_key}
        logger.info(f"get wallet address: params = '{params}'")
        return self.request(method="POST", path="/keys/address", json=params)
