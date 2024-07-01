import time

import click

from runner.logging import logger
from runner.subnets.models import AnsibleOperator
from runner.subnets.utils import pull_inventory, pull_request


@click.group(name="subnets", help="Manage IPC subnets.")
def subnets():
    pass


@subnets.command(
    name="create",
    help="Pull requests from queue and deploy subnets accordingly.",
)
def create_subnet():
    subnet_config = pull_request()
    conn_config = pull_inventory()

    operator = AnsibleOperator(subnet_config=subnet_config, conn_config=conn_config)

    operator.create_inventory()

    prepare_job_id = operator.prepare()
    operator.jobs_client.await_completion(job_id=prepare_job_id, wait_seconds=30)

    create_subnet_job_id = operator.create_subnet()
    operator.jobs_client.await_completion(job_id=create_subnet_job_id, wait_seconds=5)

    subnet_id = operator.get_subnet_id(job_id=create_subnet_job_id)
    logger.warning(
        "created subnet", subnet_id=subnet_id, project_id=operator.project_id
    )
    operator.set_subnet_id(subnet_id=subnet_id)

    copy_config_job_id = operator.copy_config()
    operator.jobs_client.await_completion(job_id=copy_config_job_id, wait_seconds=5)

    join_subnet_job_id = operator.join_subnet()
    operator.jobs_client.await_completion(job_id=join_subnet_job_id, wait_seconds=5)

    time.sleep(30)

    start_bootstrap_job_id = operator.start_bootstrap()
    operator.jobs_client.await_completion(job_id=start_bootstrap_job_id, wait_seconds=5)

    cometbft_node_id = operator.get_cometbft_node_id(job_id=start_bootstrap_job_id)
    ipld_resolver_multiaddress = operator.get_ipld_resolver_multiaddress(
        job_id=start_bootstrap_job_id
    )
    bootstrap_ip_address = operator.get_bootstrap_ip_address()

    operator.set_validator_bootstraps(
        cometbft_node_id=cometbft_node_id, ip_address=bootstrap_ip_address
    )
    operator.set_validator_resolver_bootstraps(
        multiaddr=ipld_resolver_multiaddress, ip_address=bootstrap_ip_address
    )

    start_validators_job_id = operator.start_validators()
    operator.jobs_client.await_completion(
        job_id=start_validators_job_id, wait_seconds=5
    )

    start_relayer_job_id = operator.start_relayer()
    operator.jobs_client.await_completion(job_id=start_relayer_job_id, wait_seconds=5)


@subnets.command(name="test")
def test():
    subnet_config = pull_request()
    conn_config = pull_inventory()

    job_id = "20eb8e8a37a311efaadc97857788a971"

    operator = AnsibleOperator(subnet_config=subnet_config, conn_config=conn_config)


@subnets.command(
    name="delete",
    help="Pull requests from queue and delete subnets accordingly.",
)
def delete_subnet():
    print("Delete subnet!")
