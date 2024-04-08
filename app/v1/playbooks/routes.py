from flask import jsonify

from app.v1.playbooks import playbooks_bp
from app.v1.playbooks.models import Playbook


@playbooks_bp.route("/", methods=["GET"])
def handle_list_playbooks():
    return "", 200


@playbooks_bp.route("/<playbook_name>/run", methods=["POST"])
def handle_run_playbook(playbook_name):
    playbook = Playbook(playbook_name=playbook_name, project_id="hello")
    job_id = playbook.run()

    return jsonify({"job_id": job_id}), 200
