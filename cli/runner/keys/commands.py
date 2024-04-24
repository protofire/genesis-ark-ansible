import click
from runner.keys.models import EvmKeysManager


@click.group(name="keys", help="Retrieve key info.")
def keys():
    pass


@keys.command(name="public-key", help="Retrieve public key.")
@click.argument(
    "private_key",
    type=str,
    required=True,
)
def get_public_key(private_key: str):
    evm = EvmKeysManager(private_key=private_key)
    evm.get_public_key()


@keys.command(name="address", help="Retrieve account address on the specified network.")
@click.argument(
    "private_key",
    type=str,
    required=True,
)
@click.option(
    "--network-type-for",
    "-n",
    type=str,
    required=True,
    help="Can be one of the following: test, dev, prod.",
)
def get_address(private_key: str, network_type_for: str):
    evm = EvmKeysManager(private_key=private_key)
    evm.get_address(network_type_for=network_type_for)
