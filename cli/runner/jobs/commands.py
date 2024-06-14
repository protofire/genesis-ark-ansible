import click

from runner.jobs.models import JobsClient


@click.group(name="jobs", help="Manage runner jobs.")
def jobs():
    pass


@jobs.command(
    name="status",
    help="Get status of the job specified.",
)
@click.argument(
    "job_id",
    type=str,
    required=True,
)
def get_job_status(job_id: str):
    client = JobsClient()
    client.get_status(job_id=job_id)


@jobs.command(
    name="stats",
    help="Get stats of the job specified.",
)
@click.argument(
    "job_id",
    type=str,
    required=True,
)
def get_job_stats(job_id: str):
    client = JobsClient()
    client.get_stats(job_id=job_id)


@jobs.command(
    name="events",
    help="List events of the job specified.",
)
@click.argument(
    "job_id",
    type=str,
    required=True,
)
def list_job_events(job_id: str):
    client = JobsClient()
    client.list_events(job_id=job_id)
