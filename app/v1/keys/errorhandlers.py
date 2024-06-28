from flask import jsonify

from app.v1.keys import keys_bp
from app.v1.keys.exceptions import KeysAPIException

module_info = {"endpoint": "keys", "api_version": 1}


@keys_bp.errorhandler(KeysAPIException)
def handle_api_errors(err):
    response = {"error": err.description, "message": "", **module_info, **err.extra}
    if len(err.args) > 0:
        response["message"] = err.args[0]
    return jsonify(response), err.code


@keys_bp.errorhandler(Exception)
def handle_internal_server_error(err):
    response = {"error": type(err).__name__, "message": err.message, **module_info}
    return jsonify(response), 500
