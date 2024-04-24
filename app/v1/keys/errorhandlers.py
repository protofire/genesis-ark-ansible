from flask import jsonify

from app.v1.keys import keys_bp
from app.v1.keys.exceptions import KeysAPIException


@keys_bp.errorhandler(KeysAPIException)
def handle_api_errors(err):
    response = {"error": err.description, "message": ""}
    if len(err.args) > 0:
        response["message"] = err.args[0]
    return jsonify(response), err.code


@keys_bp.errorhandler(500)
def handle_internal_server_error(err):
    response = {
        "error": "Sorry, that error is on us, please contact support if this wasn't an accident"
    }
    return jsonify(response), 500
