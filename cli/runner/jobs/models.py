import requests
from runner.logging import logger
from runner.client import Client


class JobsClient(Client):
    def get_status(self, job_id: str) -> requests.Response:
        logger.info(f"get job status: job_id = '{job_id}'")
        return self.request(method="GET", path=f"/jobs/{job_id}/status")

    def get_stats(self, job_id: str) -> requests.Response:
        logger.info(f"get job ststs: job_id = '{job_id}'")
        return self.request(method="GET", path=f"/jobs/{job_id}/stats")

    def list_events(self, job_id: str) -> requests.Response:
        logger.info(f"list job events: job_id = '{job_id}'")
        return self.request(method="GET", path=f"/jobs/{job_id}/events")
