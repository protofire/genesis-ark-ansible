import requests
from runner.logging import logger
from runner.client import Client
import time
from runner.jobs.exceptions import (
    StatsNotFoundException,
    StatusNotFoundException,
    TimeoutWaitingForCompletionException,
    JobsClientException,
)
from runner.client import safe


def exception_raiser(description: str, message: str) -> None:
    match description:
        case "stats_not_found":
            raise StatsNotFoundException(message)
        case "status_not_found":
            raise StatusNotFoundException(message)
        case _:
            raise JobsClientException(message)


class JobsClient(Client):
    @safe(exception_raiser=exception_raiser, default_exception=JobsClientException)
    def get_status(self, job_id: str) -> dict:
        logger.info(f"get job status: job_id = '{job_id}'")
        return self.request(method="GET", path=f"/jobs/{job_id}/status")

    @safe(exception_raiser=exception_raiser, default_exception=JobsClientException)
    def get_stats(self, job_id: str) -> requests.Response:
        logger.info(f"get job ststs: job_id = '{job_id}'")
        return self.request(method="GET", path=f"/jobs/{job_id}/stats")

    @safe(exception_raiser=exception_raiser, default_exception=JobsClientException)
    def list_events(self, job_id: str, events_filter: dict = {}) -> requests.Response:
        logger.info(f"list job events: job_id = '{job_id}'")
        return self.request(
            method="GET", path=f"/jobs/{job_id}/events", params=events_filter
        )

    def await_completion(
        self, job_id: str, max_attempts: int = 100, wait_seconds: int = 1
    ) -> str:
        current_attempt = 0
        while current_attempt < max_attempts:
            try:
                res = self.get_status(job_id=job_id)
                return res["status"]
            except StatusNotFoundException:
                time.sleep(wait_seconds)
                current_attempt += 1
                continue
        raise TimeoutWaitingForCompletionException(
            f"max tries reached while waiting for completion of job '{job_id}'"
        )
