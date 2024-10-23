import os

project_root = os.path.dirname(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    SECRET_KEY = os.environ.get("APP_SECRET_KEY", "dev")
    INVENTORIES_DIR = f"{project_root}/ansible/inventories"
    PRIVATE_DATA_DIR = f"{project_root}/ansible/jobs"
    PLAYBOOKS_DIR = f"{project_root}/ansible/playbooks"
    MONGO_URI = "mongodb://root:root@localhost/admin"
    ROLES_PATH = f"{project_root}/ansible/roles"
    MAINNET_RPC_URL = "https://api.node.glif.io/rpc/v1"
    CALIBNET_RPC_URL = "https://api.calibration.node.glif.io/rpc/v1"


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
