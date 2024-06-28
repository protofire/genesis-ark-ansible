from eth_keys import keys
from eth_utils import decode_hex
from web3 import Web3

from app.v1.keys.exceptions import NetworkNotConnectedException


class EvmKey:
    def __init__(self, private_key: str):
        self.private_key = private_key

    def get_public_key(self) -> str:
        priv_key_bytes = decode_hex(f"0x{self.private_key}")
        priv_key = keys.PrivateKey(priv_key_bytes)

        pub_key = priv_key.public_key
        pub_key_hex = pub_key.to_hex()

        return f"04{pub_key_hex[2:]}"

    def get_wallet_addr(self, endpoint_uri: str) -> str:
        w3 = Web3(provider=Web3.HTTPProvider(endpoint_uri=endpoint_uri))
        if not w3.is_connected():
            raise NetworkNotConnectedException(
                "failed to get wallet address: cannot connect to network by url",
                endpoint_uri=endpoint_uri,
            )

        priv_key = w3.eth.account.from_key(private_key=self.private_key)

        return priv_key.address
