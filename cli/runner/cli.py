import click
from runner.subnets.commands import subnets
from runner.gc import gc
from runner.jobs.commands import jobs
from runner.keys.commands import keys


@click.group()
def cli():
    pass


cli.add_command(subnets)
cli.add_command(gc)
cli.add_command(jobs)
cli.add_command(keys)
