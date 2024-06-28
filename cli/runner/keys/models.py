from runner.client import Client, safe
from runner.keys.exceptions import (
    KeysClientException,
    NetworkNotConnectedException,
    NetworkNotFoundException,
)
from runner.logging import logger


def exception_raiser(error: dict) -> None:
    match error["error"]:
        case "network_not_connected":
            raise NetworkNotConnectedException(**error)
        case "network_not_found":
            raise NetworkNotFoundException(**error)
        case _:
            raise KeysClientException(**error)


class KeysClient(Client):
    LOGGER_NAME = "keys"

    @safe(exception_raiser=exception_raiser, default_exception=KeysClientException)
    def get_public_key(self, private_key: str) -> dict:
        self.logger.info("computing public key", private_key=private_key)
        return self.request(
            method="POST", path="/keys/public_key", json={"privateKey": private_key}
        )

    @safe(exception_raiser=exception_raiser, default_exception=KeysClientException)
    def get_address(self, private_key: str, network_type_for: str) -> dict:
        self.logger.info(
            "retrieving wallet address",
            private_key=private_key,
            network_type_for=network_type_for,
        )
        return self.request(
            method="POST",
            path="/keys/address",
            json={"networkTypeFor": network_type_for, "privateKey": private_key},
        )
