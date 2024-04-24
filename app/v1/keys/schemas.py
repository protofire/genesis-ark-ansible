public_key_request_schema = {
    "type": "object",
    "properties": {
        "privateKey": {"type": "string"},
    },
}

address_request_schema = {
    "type": "object",
    "properties": {
        "privateKey": {"type": "string"},
        "networkTypeFor": {
            "type": "string",
            "enum": ["dev", "test", "prod"],
        },
    },
}
