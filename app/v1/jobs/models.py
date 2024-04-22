import os

from flask import current_app
from werkzeug.datastructures import ImmutableMultiDict

from app.extensions import mongo
from app.v1.jobs.exceptions import StatsNotFoundException


class EventsFilter:
    def __init__(self, args: ImmutableMultiDict):
        self.args = args

    def get_valid_params(self) -> list[str]:
        return self.get_event_data_params() + [
            "counter",
            "stdout",
            "event",
            "pid",
        ]

    def get_event_data_params(self) -> list[str]:
        return ["playbook", "play", "play_pattern", "task"]

    def convert_type(self, param: str, value: str):
        match param:
            case "counter":
                return int(value)
            case "pid":
                return int(value)
            case _:
                return value

    def dumps(self) -> dict:
        query = {}
        for param in self.args.keys():
            if param not in self.get_valid_params():
                continue

            if param not in self.get_event_data_params():
                query[param] = self.convert_type(
                    param=param, value=self.args.get(param)
                )
            else:
                query[f"event_data.{param}"] = self.convert_type(
                    param=param, value=self.args.get(param)
                )

        return query


class Job:
    def __init__(self, job_id: str):
        self.private_data_dir_root = current_app.config["PRIVATE_DATA_DIR"]
        self.job_id = job_id

    def list_events(self, events_filter: dict) -> list[dict]:
        default_query = {"runner_ident": self.job_id}
        query = events_filter | default_query
        print(query)
        events_collection = mongo.db["events"]
        return events_collection.find(query)

    def get_stats(self) -> dict:
        query = {"runner_ident": self.job_id, "event": "playbook_on_stats"}
        events_collection = mongo.db["events"]
        stats = events_collection.find_one(query)
        if stats is None:
            raise StatsNotFoundException(f"stats not found for job {self.job_id}")
        return stats

    def get_status(self) -> dict:
        status_file_path = os.path.join(
            self.private_data_dir_root, self.job_id, "artifacts", self.job_id, "status"
        )
        status = None
        with open(status_file_path, "r") as f:
            status = f.read().rstrip()
        return {"status": status}
