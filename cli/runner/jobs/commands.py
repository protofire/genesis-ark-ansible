import click

from runner.jobs.models import JobManager


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
def get_job_status(job_id):
    job = JobManager(job_id=job_id)
    job.get_status()
