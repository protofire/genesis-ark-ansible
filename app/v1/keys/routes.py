from flask import request, jsonify
from jsonschema import validate

from app.v1.keys import keys_bp
from app.v1.keys.schemas import address_request_schema, public_key_request_schema
from app.v1.keys.utils import get_network_rpc_url
from app.v1.keys.models import EvmKey


@keys_bp.route("/address", methods=["POST"])
def handle_get_address(private_key: str):
    req_json = request.get_json()
    validate(instance=req_json, schema=address_request_schema)

    network_type_for = req_json["networkTypeFor"]
    network_rpc_url = get_network_rpc_url(network_type_for=network_type_for)

    private_key = req_json["privateKey"]

    evm_key = EvmKey(private_key=private_key)
    address = evm_key.get_wallet_addr(endpoint_uri=network_rpc_url)

    return jsonify({"address": address}), 200


@keys_bp.route("/public_key", methods=["POST"])
def handle_public_key(private_key: str):
    req_json = request.get_json()
    validate(instance=req_json, schema=public_key_request_schema)

    private_key = req_json["privateKey"]

    evm_key = EvmKey(private_key=private_key)
    public_key = evm_key.get_public_key()

    return jsonify({"publicKey": public_key}), 200
