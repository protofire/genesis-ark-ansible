from flask import Blueprint

keys_bp = Blueprint("keys", __name__)

import app.v1.keys.errorhandlers  # noqa: E402, F401
import app.v1.keys.routes  # noqa: E402, F401
