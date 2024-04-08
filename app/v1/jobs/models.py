from flask import current_app
from app.extensions import mongo


class Job:
    def __init__(self, job_id):
        self.private_data_dir_root = current_app.config["PRIVATE_DATA_DIR"]
        self.job_id = job_id

    def list_events(self) -> list[dict]:
        query = {"runner_ident": self.job_id}
        events_collection = mongo.db["events"]
        return events_collection.find(query)
