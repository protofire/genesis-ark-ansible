from flask import jsonify

from app.v1.inventories import inventory_bp
from app.v1.inventories.exceptions import InventoriesAPIException


@inventory_bp.errorhandler(InventoriesAPIException)
def handle_api_errors(err):
    response = {"error": err.description, "message": ""}
    if len(err.args) > 0:
        response["message"] = err.args[0]
    return jsonify(response), err.code


@inventory_bp.errorhandler(500)
def handle_internal_server_error(err):
    response = {
        "error": "Sorry, that error is on us, please contact support if this wasn't an accident"
    }
    return jsonify(response), 500
