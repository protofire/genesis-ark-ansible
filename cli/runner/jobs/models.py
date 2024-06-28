import requests
from runner.logging import logger
from runner.client import Client
import time
from runner.jobs.exceptions import (
    StatsNotFoundException,
    StatusNotFoundException,
    TimeoutWaitingForCompletionException,
    JobsClientException,
    JobFailedException,
)
from runner.client import safe


def exception_raiser(error: dict) -> None:
    match error["error"]:
        case "stats_not_found":
            raise StatsNotFoundException(**error)
        case "status_not_found":
            raise StatusNotFoundException(**error)
        case _:
            raise JobsClientException(**error)


class JobsClient(Client):
    LOGGER_NAME = "jobs"

    @safe(exception_raiser=exception_raiser, default_exception=JobsClientException)
    def get_status(self, job_id: str) -> dict:
        self.logger.info("get job status", job_id=job_id)
        return self.request(method="GET", path=f"/jobs/{job_id}/status")

    @safe(exception_raiser=exception_raiser, default_exception=JobsClientException)
    def get_stats(self, job_id: str) -> requests.Response:
        self.logger.info("get job stats", job_id=job_id)
        return self.request(method="GET", path=f"/jobs/{job_id}/stats")

    @safe(exception_raiser=exception_raiser, default_exception=JobsClientException)
    def list_events(self, job_id: str, events_filter: dict = {}) -> requests.Response:
        self.logger.info("list job events", job_id=job_id)
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
                status = res["status"]
                if status == "failed":
                    raise JobFailedException(f"job failed: job_id = {job_id}")
                return status
            except StatusNotFoundException:
                time.sleep(wait_seconds)
                current_attempt += 1
                continue
        raise TimeoutWaitingForCompletionException(
            f"max tries reached while waiting for completion of job '{job_id}'"
        )
