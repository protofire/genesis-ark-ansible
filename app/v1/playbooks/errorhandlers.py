from flask import jsonify

from app.v1.playbooks import playbooks_bp
from app.v1.playbooks.exceptions import PlaybooksAPIException


@playbooks_bp.errorhandler(PlaybooksAPIException)
def handle_api_errors(err):
    response = {"error": err.description, "message": ""}
    if len(err.args) > 0:
        response["message"] = err.args[0]
    return jsonify(response), err.code


@playbooks_bp.errorhandler(500)
def handle_internal_server_error(err):
    response = {"error": "Sorry, that error is on us"}
    return jsonify(response), 500
