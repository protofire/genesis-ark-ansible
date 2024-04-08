import os

from flask import Flask

from app.config import DevelopmentConfig, ProductionConfig


def get_config_obj(mode):
    match mode:
        case "production":
            return ProductionConfig()
        case "development":
            return DevelopmentConfig()
        case _:
            return DevelopmentConfig()


def register_extensions(app):
    from app.extensions import mongo

    mongo.init_app(app)


def register_blueprints(app):
    from app.v1.inventories import inventory_bp
    from app.v1.playbooks import playbooks_bp
    from app.v1.jobs import jobs_bp

    app.register_blueprint(inventory_bp, url_prefix="/api/v1/inventories")
    app.register_blueprint(playbooks_bp, url_prefix="/api/v1/playbooks")
    app.register_blueprint(jobs_bp, url_prefix="/api/v1/jobs")


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app_mode = os.environ.get("APP_MODE", "development")
    app_config_obj = get_config_obj(app_mode)

    app.config.from_object(app_config_obj)
    register_extensions(app)
    register_blueprints(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
