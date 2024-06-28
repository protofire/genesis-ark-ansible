from flask import jsonify

from app.v1.inventories import inventory_bp
from app.v1.inventories.exceptions import InventoriesAPIException


module_info = {"endpoint": "inventories", "api_version": 1}


@inventory_bp.errorhandler(InventoriesAPIException)
def handle_api_errors(err):
    response = {"error": err.description, "message": "", **err.extra, **module_info}
    if len(err.args) > 0:
        response["message"] = err.args[0]
    return jsonify(response), err.code


@inventory_bp.errorhandler(500)
def handle_internal_server_error(err):
    response = {"error": type(err).__name__, "message": err.message, **module_info}
    return jsonify(response), 500
