import click
from runner.subnets.commands import subnets
from runner.gc import gc
from runner.jobs.commands import jobs


@click.group()
def cli():
    pass


cli.add_command(subnets)
cli.add_command(gc)
cli.add_command(jobs)
