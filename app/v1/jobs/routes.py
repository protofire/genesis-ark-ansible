from bson.json_util import dumps
from flask import Response

from app.v1.jobs import jobs_bp
from app.v1.jobs.models import Job


@jobs_bp.route("/<job_id>/events", methods=["GET"])
def handle_list_job_events(job_id):
    job = Job(job_id=job_id)
    events = job.list_events()

    payload = dumps(events)
    res = Response(payload)
    res.headers["Content-Type"] = "application/json"
    return res


@jobs_bp.route("/<job_id>/events/<event_id>", methods=["GET"])
def handle_get_job_event(job_id, event_id):
    pass
