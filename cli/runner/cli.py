import click

from runner.gc import gc
from runner.jobs.commands import jobs
from runner.jobs.exceptions import (
    JobsClientException,
    StatsNotFoundException,
    StatusNotFoundException,
    TimeoutWaitingForCompletionException,
)
from runner.keys.commands import keys
from runner.logging import logger
from runner.subnets.commands import subnets


@click.group()
def cli():
    pass


cli.add_command(subnets)
cli.add_command(gc)
cli.add_command(jobs)
cli.add_command(keys)


def safe_entrypoint():
    try:
        cli()
    except (
        StatsNotFoundException,
        StatusNotFoundException,
        JobsClientException,
        TimeoutWaitingForCompletionException,
    ) as e:
        logger.error(e)
