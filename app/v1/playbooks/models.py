import os
import uuid

from ansible_runner import run_async
from flask import current_app
from app.v1.playbooks.exceptions import PlaybookNotFoundException
from app.extensions import mongo


def event_handler(event_data):
    print(event_data)
    events_collection = mongo.db["events"]
    events_collection.insert_one(dict(event_data))
    return False


class Playbook:
    def __init__(self, playbook_name, project_id):
        self.playbook_name = playbook_name
        self.project_id = project_id
        self.playbooks_dir = current_app.config["PLAYBOOKS_DIR"]
        self.roles_dir = current_app.config["ROLES_PATH"]
        self.playbook_path = os.path.join(self.playbooks_dir, playbook_name)

    def is_exists(self):
        return os.path.exists(self.playbook_path)

    def run(self, tags=None, extra_vars=None):
        if not self.is_exists():
            raise PlaybookNotFoundException(
                "failed to run playbook: playbook not found",
                playbook_name=self.playbook_name,
                project_id=self.project_id,
                playbooks_dir=self.playbooks_dir,
                roles_dir=self.roles_dir,
                playbook_path=self.playbook_path,
                tags=tags,
                extra_vars=extra_vars,
            )

        job_id = str(uuid.uuid1().hex)

        private_data_dir_root = current_app.config["PRIVATE_DATA_DIR"]
        private_data_dir = os.path.join(private_data_dir_root, job_id)
        os.makedirs(private_data_dir)

        inventories_dir = current_app.config["INVENTORIES_DIR"]
        inventory_path = os.path.join(inventories_dir, f"{self.project_id}.yaml")

        run_async(
            private_data_dir=private_data_dir,
            suppress_ansible_output=True,
            inventory=inventory_path,
            playbook=self.playbook_path,
            extravars=extra_vars,
            tags=tags,
            ident=job_id,
            event_handler=event_handler,
            roles_path=self.roles_dir,
        )

        return job_id
