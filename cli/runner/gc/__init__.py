import click
from runner.gc.artifacts import rotate_artifacts


@click.group(name="gc", help="Manage garbage collection.")
def gc():
    pass


@gc.command(
    name="artifacts",
    help="Initiates the garbage collection process for artifacts.",
)
@click.option(
    "--max-age-days",
    "-d",
    default=3,
    type=int,
    help="Set the maximum age (in days) of artifacts to retain. Artifacts exceeding this age will be considered for garbage collection.",
)
def artifacts(max_age_days):
    rotate_artifacts(max_age_days)


@gc.command(
    name="events",
    help="Initiates the garbage collection process for events.",
)
@click.option(
    "--max-age-days",
    "-d",
    default=3,
    type=int,
    help="Set the maximum age (in days) of events to retain. Events exceeding this age will be considered for garbage collection.",
)
def events(max_age_days):
    print(f"Delete events older than {max_age_days}!")
