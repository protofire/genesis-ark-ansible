import click
from runner.subnets.commands import subnets
from runner.gc import gc


@click.group()
def cli():
    pass


cli.add_command(subnets)
cli.add_command(gc)
