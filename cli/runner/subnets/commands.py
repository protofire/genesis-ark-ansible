import click
from jsonschema import validate

from runner.subnets.models import SubnetManager
from runner.subnets.schemas import infra_schema, network_schema
from runner.subnets.utils import pull_inventory, pull_request


@click.group(name="subnets", help="Manage IPC subnets.")
def subnets():
    pass


@subnets.command(
    name="create",
    help="Pull requests from queue and deploy subnets accordingly.",
)
def create_subnet():
    # Pull subnet configuration schema
    subnet_config = pull_request()
    validate(instance=subnet_config, schema=network_schema)

    # Pull infrastructure configuration
    infra_config = pull_inventory()
    validate(instance=infra_config, schema=infra_schema)

    sm = SubnetManager(infra_config=infra_config, subnet_config=subnet_config)
    sm.populate_inventory()
    job_id = sm.run_prepare()


@subnets.command(
    name="delete",
    help="Pull requests from queue and delete subnets accordingly.",
)
def delete_subnet():
    print("Delete subnet!")
