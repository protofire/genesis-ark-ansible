from flask import jsonify, request

from app.v1.playbooks import playbooks_bp
from app.v1.playbooks.models import Playbook


@playbooks_bp.route("/", methods=["GET"])
def handle_list_playbooks():
    return "", 200


@playbooks_bp.route("/<playbook_name>/run", methods=["POST"])
def handle_run_playbook(playbook_name):
    payload = request.json
    extra_vars = payload.get("extra_vars", None)
    tags = payload.get("tags", None)

    playbook = Playbook(playbook_name=playbook_name, project_id="hello")
    job_id = playbook.run(extra_vars=extra_vars, tags=tags)

    return jsonify({"job_id": job_id}), 200
