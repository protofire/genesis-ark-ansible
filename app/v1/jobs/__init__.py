from flask import Blueprint

jobs_bp = Blueprint("jobs", __name__)

import app.v1.jobs.errorhandlers  # noqa: E402, F401
import app.v1.jobs.routes  # noqa: E402, F401
