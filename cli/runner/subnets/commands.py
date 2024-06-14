import re

import click

from runner.inventories.models import InvenentoriesClient
from runner.jobs.models import JobsClient
from runner.logging import logger
from runner.playbooks.models import PlaybooksClient
from runner.subnets.utils import pull_inventory, pull_request
from runner.subnets.models import AnsibleOperator


def get_subnet_id(string: str) -> str:
    pattern = r".*created subnet actor with id: (.*)"
    found = re.findall(pattern=pattern, string=string)
    full_subnet_id = found[0]
    chunks = full_subnet_id.split("/")
    print(chunks[-1])


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

    playbooks_client = PlaybooksClient()
    jobs_client = JobsClient()


#    # run prepare phase on all validators
#    prepare_res = playbooks_client.prepare(
#        project_id=project_id, extra_vars={"var_host": "validators"}
#    )
#    prepare_json = prepare_res.json()
#    job_id = prepare_json["job_id"]
#    status = jobs_client.await_completion(job_id=job_id, wait_seconds=5)
#    if status != "successful":
#        # TODO: do something meaningful
#        return 1
#
#    create_subnet_res = playbooks_client.create_subnet(
#        project_id=project_id, extra_vars={"var_host": "bootstraps"}
#    )
#    create_subnet_json = create_subnet_res.json()
#    job_id = create_subnet_json["job_id"]
#    status = jobs_client.await_completion(job_id=job_id, wait_seconds=5)
#    if status != "successful":
#        # TODO: do something meaningful
#        return 1
#
#    events_res = jobs_client.list_events(
#        job_id=job_id,
#        events_filter={"event": "runner_on_ok", "task": "Print create subnet output"},
#    )
#    events_json = events_res.json()
#    # TODO: add check if event exists
#    event = events_json[0]
#    result_line = event["event_data"]["res"]["msg"]["stderr_lines"][-1]
#    subnet_id = get_subnet_id(string=result_line)
#    print(subnet_id)
#    # TODO: add check if that's a valid subnet id
#
#    inventories_client.set_group_vars(
#        project_id=project_id,
#        group_name="validators",
#        group_vars={"validator_subnet_id": subnet_id},
#    )
#
#    copy_config_res = playbooks_client.copy_config(
#        project_id=project_id, extra_vars={"var_host": "validators"}
#    )
#    copy_config_json = copy_config_res.json()
#    job_id = copy_config_json["job_id"]
#
#    status = jobs_client.await_completion(job_id=job_id, wait_seconds=5)
#


@subnets.command(
    name="delete",
    help="Pull requests from queue and delete subnets accordingly.",
)
def delete_subnet():
    print("Delete subnet!")
