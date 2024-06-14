import requests

from runner.client import Client, safe
from runner.playbooks.exceptions import (
    PlaybookNotFoundException,
    PlaybooksClientException,
)


def exception_raiser(error_description: str, error_message: str) -> None:
    match error_description:
        case "playbook_not_found":
            raise PlaybookNotFoundException(error_message)
        case _:
            raise PlaybooksClientException(error_message)


class PlaybooksClient(Client):
    VALIDATOR_PLAYBOOK_NAME = "validator.yaml"

    @safe(exception_raiser=exception_raiser, default_exception=PlaybooksClientException)
    def run_playbook(
        self,
        playbook_name: str,
        project_id: str,
        extra_vars: dict = {},
        tags: list = [],
    ) -> requests.Response:
        payload = {"extra_vars": extra_vars, "tags": ",".join(tags)}
        return self.request(
            method="POST",
            path=f"/playbooks/{playbook_name}/projects/{project_id}/run",
            json=payload,
        )

    def prepare(self, project_id: str, extra_vars: dict = {}) -> requests.Response:
        return self.run_playbook(
            playbook_name=self.VALIDATOR_PLAYBOOK_NAME,
            project_id=project_id,
            extra_vars=extra_vars,
            tags=["validator:prepare"],
        )

    def create_subnet(
        self, project_id: str, extra_vars: dict = {}
    ) -> requests.Response:
        return self.run_playbook(
            playbook_name=self.VALIDATOR_PLAYBOOK_NAME,
            project_id=project_id,
            extra_vars=extra_vars,
            tags=["validator:create_subnet"],
        )

    def join_subnet(self, project_id: str, extra_vars: dict = {}) -> requests.Response:
        return self.run_playbook(
            playbook_name=self.VALIDATOR_PLAYBOOK_NAME,
            project_id=project_id,
            extra_vars=extra_vars,
            tags=["validator:join_subnet"],
        )

    def start_bootstrap(
        self, project_id: str, extra_vars: dict = {}
    ) -> requests.Response:
        return self.run_playbook(
            playbook_name=self.VALIDATOR_PLAYBOOK_NAME,
            project_id=project_id,
            extra_vars=extra_vars,
            tags=["validator:start_bootstrap"],
        )

    def start_validator(
        self, project_id: str, extra_vars: dict = {}
    ) -> requests.Response:
        return self.run_playbook(
            playbook_name=self.VALIDATOR_PLAYBOOK_NAME,
            project_id=project_id,
            extra_vars=extra_vars,
            tags=["validator:start"],
        )

    def copy_config(self, project_id: str, extra_vars: dict = {}) -> requests.Response:
        return self.run_playbook(
            playbook_name=self.VALIDATOR_PLAYBOOK_NAME,
            project_id=project_id,
            extra_vars=extra_vars,
            tags=["validator:copy_config"],
        )

    def start_relayer(
        self, project_id: str, extra_vars: dict = {}
    ) -> requests.Response:
        return self.run_playbook(
            playbook_name=self.VALIDATOR_PLAYBOOK_NAME,
            project_id=project_id,
            extra_vars=extra_vars,
            tags=["validator:start_relayer"],
        )
