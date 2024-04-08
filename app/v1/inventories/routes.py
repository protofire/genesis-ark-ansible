from flask import jsonify, request

from app.v1.inventories import inventory_bp
from app.v1.inventories.models import Inventory


@inventory_bp.route("/<project_id>/groups", methods=["GET"])
def handle_list_groups(project_id):
    inventory = Inventory(project_id=project_id)
    inventory.load()

    groups = inventory.list_group_names()

    return jsonify(groups), 200


@inventory_bp.route("/<project_id>/groups/<group_name>/hosts", methods=["GET"])
def handle_list_group_hosts(project_id, group_name):
    inventory = Inventory(project_id=project_id)
    inventory.load()

    group_hosts = inventory.list_group_hosts_names()

    return jsonify(group_hosts), 200


@inventory_bp.route("/<project_id>/groups/<group_name>", methods=["POST"])
def handle_add_group(project_id, group_name):
    inventory = Inventory(project_id=project_id)
    inventory.load()

    inventory.add_group(group_name=group_name)
    inventory.save()

    return "", 200


@inventory_bp.route("/<project_id>/groups/<group_name>", methods=["DELETE"])
def handle_delete_group(project_id, group_name):
    inventory = Inventory(project_id=project_id)
    inventory.load()

    inventory.delete_group(group_name=group_name)
    inventory.save()

    return "", 200


@inventory_bp.route("/<project_id>/hosts", methods=["GET"])
def handle_list_hosts(project_id):
    inventory = Inventory(project_id=project_id)
    inventory.load()

    hosts = inventory.list_host_names()

    return jsonify(hosts), 200


@inventory_bp.route("/<project_id>/hosts/<host_name>/groups", methods=["GET"])
def handle_list_host_groups(project_id, host_name):
    inventory = Inventory(project_id=project_id)
    inventory.load()

    host_groups = inventory.list_host_groups_names(host_name=host_name)

    return jsonify(host_groups), 200


@inventory_bp.route("/<project_id>/hosts/<host_name>", methods=["DELETE"])
def handle_delete_host(project_id, host_name):
    inventory = Inventory(project_id=project_id)
    inventory.load()

    inventory.delete_host(host_name=host_name)
    inventory.save()

    return "", 200


@inventory_bp.route(
    "/<project_id>/hosts/<host_name>/groups/<group_name>", methods=["POST"]
)
@inventory_bp.route(
    "/<project_id>/groups/<group_name>/hosts/<host_name>", methods=["POST"]
)
def handle_add_host_to_group(project_id, host_name, group_name):
    inventory = Inventory(project_id=project_id)
    inventory.load()

    inventory.add_group_host(group_name=group_name, host_name=host_name)
    inventory.save()

    return "", 200


@inventory_bp.route(
    "/<project_id>/hosts/<host_name>/groups/<group_name>", methods=["DELETE"]
)
def handle_delete_host_from_group(project_id, host_name, group_name):
    inventory = Inventory(project_id=project_id)
    inventory.load()

    inventory.delete_group_host(group_name=group_name, host_name=host_name)
    inventory.save()

    return "", 200


@inventory_bp.route(
    "/<project_id>/groups/<group_name>/hosts/<host_name>/vars", methods=["GET"]
)
def handle_list_host_vars(project_id, group_name, host_name):
    inventory = Inventory(project_id=project_id)
    inventory.load()

    host_vars = inventory.get_group_host_vars(
        group_name=group_name, host_name=host_name
    )

    return jsonify(host_vars), 200


@inventory_bp.route(
    "/<project_id>/groups/<group_name>/hosts/<host_name>/vars",
    methods=["DELETE"],
)
def handle_delete_host_vars(project_id, group_name, host_name):
    inventory = Inventory(project_id=project_id)
    inventory.load()

    inventory.delete_group_host_vars(group_name=group_name, host_name=host_name)
    inventory.save()

    return "", 200


@inventory_bp.route(
    "/<project_id>/groups/<group_name>/hosts/<host_name>/vars",
    methods=["POST"],
)
def handle_set_host_vars(project_id, group_name, host_name):
    host_vars = request.json

    inventory = Inventory(project_id=project_id)
    inventory.load()

    inventory.set_group_host_vars(
        group_name=group_name, host_name=host_name, host_vars=host_vars
    )
    inventory.save()

    return "", 200


@inventory_bp.route("/<project_id>/groups/<group_name>/vars", methods=["GET"])
def handle_list_group_vars(project_id, group_name):
    inventory = Inventory(project_id=project_id)
    inventory.load()

    group_vars = inventory.get_group_vars(group_name=group_name)

    return jsonify(group_vars), 200


@inventory_bp.route("/<project_id>/groups/<group_name>/vars", methods=["DELETE"])
def handle_delete_group_vars(project_id, group_name):
    inventory = Inventory(project_id=project_id)
    inventory.load()

    inventory.delete_group_vars(group_name=group_name)
    inventory.save()

    return "", 200


@inventory_bp.route("/<project_id>/groups/<group_name>/vars", methods=["POST"])
def handle_set_group_vars(project_id, group_name):
    group_vars = request.json

    inventory = Inventory(project_id=project_id)
    inventory.load()

    inventory.set_group_vars(group_name=group_name, group_vars=group_vars)
    inventory.save()

    return "", 200
