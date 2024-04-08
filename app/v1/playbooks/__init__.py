from flask import Blueprint

playbooks_bp = Blueprint("playbooks", __name__)

import app.v1.playbooks.errorhandlers  # noqa: E402, F401
import app.v1.playbooks.routes  # noqa: E402, F401
