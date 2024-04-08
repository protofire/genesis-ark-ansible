from flask import Blueprint

inventory_bp = Blueprint("inventory", __name__)

import app.v1.inventories.errorhandlers  # noqa: E402, F401
import app.v1.inventories.routes  # noqa: E402, F401
