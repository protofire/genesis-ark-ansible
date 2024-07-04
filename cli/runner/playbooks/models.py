import requests

from runner.client import Client, safe
from runner.playbooks.exceptions import (
    PlaybookNotFoundException,
    PlaybooksClientException,
)


def exception_raiser(error: dict) -> None:
    match error["error"]:
        case "playbook_not_found":
            raise PlaybookNotFoundException(**error)
        case _:
            raise PlaybooksClientException(**error)


class PlaybooksClient(Client):
    LOGGER_NAME = "playbooks"
    VALIDATOR_PLAYBOOK_NAME = "validator.yaml"

    @safe(exception_raiser=exception_raiser, default_exception=PlaybooksClientException)
    def run_playbook(
        self,
        playbook_name: str,
        project_id: str,
        extra_vars: dict = {},
        tags: list = [],
    ) -> dict:
        self.logger.info(
            "run playbook",
            playbook_name=playbook_name,
            project_id=project_id,
            extra_vars=extra_vars,
            tags=tags,
        )
        payload = {"extra_vars": extra_vars, "tags": ",".join(tags)}
        return self.request(
            method="POST",
            path=f"/playbooks/{playbook_name}/projects/{project_id}/run",
            json=payload,
        )

    def prepare(self, project_id: str, extra_vars: dict = {}) -> dict:
        return self.run_playbook(
            playbook_name=self.VALIDATOR_PLAYBOOK_NAME,
            project_id=project_id,
            extra_vars=extra_vars,
            tags=["validator:prepare"],
        )

    def create_subnet(self, project_id: str, extra_vars: dict = {}) -> dict:
        return self.run_playbook(
            playbook_name=self.VALIDATOR_PLAYBOOK_NAME,
            project_id=project_id,
            extra_vars=extra_vars,
            tags=["validator:create_subnet"],
        )

    def join_subnet(self, project_id: str, extra_vars: dict = {}) -> dict:
        return self.run_playbook(
            playbook_name=self.VALIDATOR_PLAYBOOK_NAME,
            project_id=project_id,
            extra_vars=extra_vars,
            tags=["validator:join_subnet"],
        )

    def prune(self, project_id: str, extra_vars: dict = {}) -> dict:
        return self.run_playbook(
            playbook_name=self.VALIDATOR_PLAYBOOK_NAME,
            project_id=project_id,
            extra_vars=extra_vars,
            tags=["validator:prune"],
        )

    def start_bootstrap(self, project_id: str, extra_vars: dict = {}) -> dict:
        return self.run_playbook(
            playbook_name=self.VALIDATOR_PLAYBOOK_NAME,
            project_id=project_id,
            extra_vars=extra_vars,
            tags=["validator:start_bootstrap"],
        )

    def start_validator(self, project_id: str, extra_vars: dict = {}) -> dict:
        return self.run_playbook(
            playbook_name=self.VALIDATOR_PLAYBOOK_NAME,
            project_id=project_id,
            extra_vars=extra_vars,
            tags=["validator:start"],
        )

    def copy_config(self, project_id: str, extra_vars: dict = {}) -> dict:
        return self.run_playbook(
            playbook_name=self.VALIDATOR_PLAYBOOK_NAME,
            project_id=project_id,
            extra_vars=extra_vars,
            tags=["validator:copy_config"],
        )

    def start_relayer(self, project_id: str, extra_vars: dict = {}) -> dict:
        return self.run_playbook(
            playbook_name=self.VALIDATOR_PLAYBOOK_NAME,
            project_id=project_id,
            extra_vars=extra_vars,
            tags=["validator:start_relayer"],
        )
