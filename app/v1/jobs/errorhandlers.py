from flask import jsonify

from app.v1.jobs import jobs_bp
from app.v1.jobs.exceptions import JobsAPIException

module_info = {"endpoint": "jobs", "api_version": 1}


@jobs_bp.errorhandler(JobsAPIException)
def handle_api_errors(err):
    response = {"error": err.description, "message": "", **module_info, **err.extra}
    if len(err.args) > 0:
        response["message"] = err.args[0]
    return jsonify(response), err.code


@jobs_bp.errorhandler(500)
def handle_internal_server_error(err):
    response = {"error": type(err).__name__, "message": err.message, **module_info}
    return jsonify(response), 500
