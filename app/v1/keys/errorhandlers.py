from flask import jsonify

from app.v1.keys import keys_bp
from app.v1.keys.exceptions import KeysAPIException


@keys_bp.errorhandler(KeysAPIException)
def handle_api_errors(err):
    response = {"error": err.description, "message": ""}
    if len(err.args) > 0:
        response["message"] = err.args[0]
    return jsonify(response), err.code


@keys_bp.errorhandler(Exception)
def handle_internal_server_error(err):
    response = {"error": type(err).__name__, "message": err.message}
    return jsonify(response), 500
