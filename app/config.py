import os


class Config(object):
    DEBUG = False
    SECRET_KEY = os.environ.get("APP_SECRET_KEY", "dev")
    INVENTORIES_DIR = "/home/ubuntu/work/ipc/flask-runner/ansible/inventories"
    PRIVATE_DATA_DIR = "/home/ubuntu/work/ipc/flask-runner/ansible/jobs"
    PLAYBOOKS_DIR = "/home/ubuntu/work/ipc/flask-runner/ansible/playbooks"
    MONGO_URI = "mongodb://root:root@localhost/admin"
    ROLES_PATH = "/home/ubuntu/work/ipc/flask-runner/ansible/roles"
    MAINNET_RPC_URL = "https://api.node.glif.io/rpc/v1"
    CALIBNET_RPC_URL = "https://api.calibration.node.glif.io/rpc/v1"


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
