import os


class Config(object):
    DEBUG = False
    SECRET_KEY = os.environ.get("APP_SECRET_KEY", "dev")
    INVENTORIES_DIR = "/home/ubuntu/work/ipc/flask-runner/ansible/inventories"
    PRIVATE_DATA_DIR = "/home/ubuntu/work/ipc/flask-runner/ansible/jobs"
    PLAYBOOKS_DIR = "/home/ubuntu/work/ipc/flask-runner/ansible/playbooks"
    MONGO_URI = "mongodb://root:root@localhost/admin"


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
