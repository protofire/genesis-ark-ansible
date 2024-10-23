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
@click.option(
    "--skip-prepare",
    is_flag=True,
    default=False,
    show_default=True,
    help="Skip dependencies installation",
)
def create_subnet(skip_prepare: bool):
    subnet_config = pull_request()
    conn_config = pull_inventory()

    operator = AnsibleOperator(subnet_config=subnet_config, conn_config=conn_config)

    operator.create_inventory()

    if not skip_prepare:
        prepare_job_id = operator.prepare()
        operator.jobs_client.await_completion(job_id=prepare_job_id, wait_seconds=30)
    
    copy_config_job_id = operator.copy_config()
    operator.jobs_client.await_completion(job_id=copy_config_job_id, wait_seconds=5)

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

    operator.set_bootstraps(
        cometbft_node_id=cometbft_node_id,
        ip_address=bootstrap_ip_address,
        multiaddr=ipld_resolver_multiaddress,
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


@subnets.command(name="install-blockscout")
def install_blockscout():
    subnet_config = pull_request()
    conn_config = pull_inventory()

    operator = AnsibleOperator(subnet_config=subnet_config, conn_config=conn_config)

    operator.create_inventory()

    install_blockscout_job_id = operator.install_blockscout()
    operator.jobs_client.await_completion(
        job_id=install_blockscout_job_id, wait_seconds=5
    )


@subnets.command(name="reset-blockscout")
def reset_blockscout():
    subnet_config = pull_request()
    conn_config = pull_inventory()

    operator = AnsibleOperator(subnet_config=subnet_config, conn_config=conn_config)

    operator.create_inventory()

    reset_blockscout_job_id = operator.reset_blockscout()
    operator.jobs_client.await_completion(
        job_id=reset_blockscout_job_id, wait_seconds=5
    )


@subnets.command(name="update-blockscout")
def update_blockscout():
    subnet_config = pull_request()
    conn_config = pull_inventory()

    operator = AnsibleOperator(subnet_config=subnet_config, conn_config=conn_config)

    operator.create_inventory()

    update_blockscout_job_id = operator.update_blockscout()
    operator.jobs_client.await_completion(
        job_id=update_blockscout_job_id, wait_seconds=5
    )


@subnets.command(
    name="delete",
    help="Pull requests from queue and delete subnets accordingly.",
)
def delete_subnet():
    subnet_config = pull_request()
    conn_config = pull_inventory()

    operator = AnsibleOperator(subnet_config=subnet_config, conn_config=conn_config)
    prune_job_id = operator.prune()
    operator.jobs_client.await_completion(job_id=prune_job_id, wait_seconds=5)
