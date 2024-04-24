from flask import current_app
from app.v1.keys.exceptions import NetworkNotFoundException


def get_network_rpc_url(network_type_for: str) -> str:
    match network_type_for:
        case "dev":
            return current_app.config["CALIBNET_RPC_URL"]
        case "test":
            return current_app.config["CALIBNET_RPC_URL"]
        case "prod":
            return current_app.config["MAINNET_RPC_URL"]
        case _:
            raise NetworkNotFoundException(
                f"cannot determine RPC URL based on 'networkTypeFor': {network_type_for}"
            )
