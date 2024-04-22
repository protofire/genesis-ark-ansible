node_schema = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "id",
        "isArchive",
        "name",
        "cpu",
        "memory",
        "location",
        "cloud",
        "createdAt",
        "updatedAt",
    ],
    "properties": {
        "id": {"type": "number"},
        "PrivateKey": {"type": "string"},
        "stake": {"type": "number"},
        "isArchive": {"type": "boolean"},
        "name": {"type": "string"},
        "cpu": {"type": "string"},
        "memory": {"type": "string"},
        "location": {"type": "string"},
        "cloud": {"type": "string"},
        "networkId": {"type": "number"},
        "createdAt": {"type": "string"},
        "updatedAt": {"type": "string"},
    },
}


network_schema = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "id",
        "appChainName",
        "networkTypeFor",
        "isPrivate",
        "networkType",
        "minStake",
        "bottomUp",
        "topDown",
        "state",
        "userId",
        "nodes",
    ],
    "properties": {
        "id": {"type": "number"},
        "appChainName": {"type": "string"},
        "networkId": {"type": "number"},
        "networkTypeFor": {"type": "string"},
        "isPrivate": {"type": "boolean"},
        "publicName": {"type": "string"},
        "description": {"type": "string"},
        "website": {"type": "string"},
        "networkType": {"type": "string"},
        "minStake": {"type": "number"},
        "bottomUp": {"type": "number"},
        "topDown": {"type": "number"},
        "state": {"type": "string"},
        "userId": {"type": "number"},
        "createdAt": {"type": "string"},
        "updatedAt": {"type": "string"},
        "nodes": {"type": "array", "items": node_schema},
    },
}

instance_connection_schema = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "nodeId",
        "ipAddress",
    ],
    "properties": {
        "nodeId": {"type": "number"},
        "ipAddress": {"type": "string"},
    },
}

infra_schema = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "_id",
        "customer_id",
        "project_id",
        "infrastructurestatus",
        "instanceconnections",
    ],
    "properties": {
        "_id": {"type": "string"},
        "customer_id": {"type": "number"},
        "project_id": {"type": "number"},
        "infrastructurestatus": {"type": "string"},
        "instanceconnections": {
            "type": "array",
            "items": instance_connection_schema,
        },
    },
}
