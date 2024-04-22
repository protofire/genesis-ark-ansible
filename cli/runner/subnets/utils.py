def pull_request():
    return {
        "id": 1,
        "appChainName": "test",
        "networkTypeFor": "test",
        "isPrivate": False,
        "networkType": "fvm",
        "minStake": 1,
        "bottomUp": 30,
        "topDown": 30,
        "state": "inProgress",
        "userId": 1,
        "nodes": [
            {
                "id": 1,
                "isArchive": False,
                "name": "validator_1",
                "cpu": "1",
                "memory": "2",
                "location": "us-east-1",
                "cloud": "AWS",
                "createdAt": "2024-04-18T09:56:59.418Z",
                "updatedAt": "2024-04-18T09:56:59.418Z",
                "PrivateKey": "205b6a95f7b4f2618a73faa112e909059cd97e0215d58177b31f92f6b5901032",
                "stake": 1,
            },
            {
                "id": 2,
                "isArchive": False,
                "name": "validator_2",
                "cpu": "1",
                "memory": "2",
                "location": "us-east-1",
                "cloud": "AWS",
                "createdAt": "2024-04-18T09:56:59.418Z",
                "updatedAt": "2024-04-18T09:56:59.418Z",
                "PrivateKey": "205b6a95f7b4f2618a73faa112e909059cd97e0215d58177b31f92f6b5901032",
                "stake": 1,
            },
            {
                "id": 3,
                "isArchive": False,
                "name": "validator_3",
                "cpu": "1",
                "memory": "2",
                "location": "us-east-1",
                "cloud": "AWS",
                "createdAt": "2024-04-18T09:56:59.418Z",
                "updatedAt": "2024-04-18T09:56:59.418Z",
                "PrivateKey": "205b6a95f7b4f2618a73faa112e909059cd97e0215d58177b31f92f6b5901032",
                "stake": 1,
            },
            {
                "id": 4,
                "isArchive": False,
                "name": "validator_2",
                "cpu": "1",
                "memory": "2",
                "location": "us-east-1",
                "cloud": "AWS",
                "createdAt": "2024-04-18T09:56:59.418Z",
                "updatedAt": "2024-04-18T09:56:59.418Z",
                "PrivateKey": "205b6a95f7b4f2618a73faa112e909059cd97e0215d58177b31f92f6b5901032",
                "stake": 4,
            },
        ],
    }


def pull_inventory():
    return {
        "_id": "1",
        "project_id": 1,
        "customer_id": 1,
        "infrastructurestatus": "CREATION_INITIALIZED",
        "instanceconnections": [
            {
                "nodeId": 1,
                "ipAddress": "127.0.0.1",
            },
            {
                "nodeId": 2,
                "ipAddress": "127.0.0.1",
            },
            {
                "nodeId": 3,
                "ipAddress": "127.0.0.1",
            },
            {
                "nodeId": 4,
                "ipAddress": "127.0.0.1",
            },
        ],
    }
