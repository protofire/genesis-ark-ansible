from bson.json_util import dumps
from flask import Response, request

from app.v1.jobs import jobs_bp
from app.v1.jobs.models import Job, EventsFilter


@jobs_bp.route("/<job_id>/events", methods=["GET"])
def handle_list_job_events(job_id):
    job = Job(job_id=job_id)

    events_filter = EventsFilter(request.args)
    events = job.list_events(events_filter=events_filter.dumps())

    payload = dumps(events)
    res = Response(payload)
    res.headers["Content-Type"] = "application/json"
    return res


@jobs_bp.route("/<job_id>/stats", methods=["GET"])
def handle_get_stats(job_id):
    job = Job(job_id=job_id)
    stats = job.get_stats()

    payload = dumps(stats)
    res = Response(payload)
    res.headers["Content-Type"] = "application/json"
    return res


@jobs_bp.route("/<job_id>/status", methods=["GET"])
def handle_get_status(job_id):
    job = Job(job_id=job_id)
    status = job.get_status()
    return status, 200
