import requests
from runner.logging import logger, log_response_hook


class SubnetManager:
    GROUP_VALIDATORS = "validators"
    GROUP_BOOTSTRAPS = "bootstraps"
    GROUP_NON_BOOTSTRAPS = "non_bootstraps"

    def __init__(
        self,
        infra_config: dict,
        subnet_config: dict,
        api_url="http://localhost:5000/api/v1",
    ):
        self.api_url = api_url
        self.infra_config = infra_config
        self.subnet_config = subnet_config
        self.project_id = self.get_project_id()

    def get_project_id(self):
        return self.subnet_config["id"]

    def make_host_vars(self) -> dict:
        example = {
            "validator_name": "",
            "validator_private_key_path": "",
            "validator_parent_subnet_id": "",
            "validator_subnet_id": "",
            "validator_cmt_p2p_host_port": "",
            "validator_cmt_rpc_host_port": "",
            "validator_ethapi_host_port": "",
            "validator_resolver_host_port": "",
            "validator_parent_registry": "",
            "validator_parent_gateway": "",
            "validator_min_validator_stake": "",
            "validator_min_validators": "",
            "validator_bottom_check_period": "",
            "validator_permission_mode": "",
            "validator_supply_source_kind": "",
            "validator_default_address": "",
            "validator_secrets": "",
            "validator_bootstraps": "",
            "validator_resolver_bootstraps": "",
        }
        return {}

    def is_validator(self, node: dict) -> bool:
        """Determine if the given node is a validator.

        Args:
            node (dict): A node from the subnet config.

        Returns:
            bool: 'True' if the node is a validator, 'False' otherwise.
        """
        return "PrivateKey" in node and "stake" in node

    def merge_hosts_data(self) -> list[dict]:
        """Merges nodes data from 'subnet_config' with connection details from 'infra_config'.
        Applies to validator nodes only.

        Returns:
            list[dict]: List of hosts in the following format: '{"node": node_data, "conn": connection_details}'.
        """
        hosts = []
        for node in self.subnet_config["nodes"]:
            # Skip node if it's not a validator
            if not self.is_validator(node):
                continue

            # Search for connection details based on node ID. If connection details not found, return None.
            node_conn = next(
                (
                    conn
                    for conn in self.infra_config["instanceconnections"]
                    if conn["nodeId"] == node["id"]
                ),
                None,
            )
            if node_conn is None:
                continue

            host = {"node": node, "conn": node_conn}
            hosts.append(host)
        return hosts

    def create_group(self, group_name: str) -> requests.Response:
        """Add group to the project's inventory file.

        Args:
            group_name (str): Group name to add.

        Returns:
            requests.Response: Result of the operation.
        """
        params = {
            "project_id": self.project_id,
            "group_name": group_name,
        }
        logger.info(f"add group: params = '{params}'")
        return self._request(
            method="POST",
            path=f"/inventories/{self.project_id}/groups/{group_name}",
        )

    def add_host_to_group(self, group_name: str, host_name: str) -> requests.Response:
        """Add host to the specified group of the project's inventory file.

        Args:
            group_name (str): Target group name.
            host_name (str): Host name to add.

        Returns:
            requests.Response: Result of the operation.
        """
        params = {
            "project_id": self.project_id,
            "group_name": group_name,
            "host_name": host_name,
        }
        logger.info(f"add host: params = '{params}'")
        return self._request(
            method="POST",
            path=f"/inventories/{self.project_id}/groups/{group_name}/hosts/{host_name}",
        )

    def set_host_vars(
        self, group_name: str, host_name: str, host_vars: dict
    ) -> requests.Response:
        """Assign variables to the specified host within the designated group of the project's inventory file.

        Args:
            group_name (str): Target group name.
            host_name (str): Target host name.
            host_vars (dict): Host variables.

        Returns:
            requests.Response: Result of the operation.
        """
        params = {
            "project_id": self.project_id,
            "group_name": group_name,
            "host_name": host_name,
            "host_vars": host_vars,
        }
        logger.info(f"add host vars: params = '{params}'")
        return self._request(
            method="POST",
            path=f"/inventories/{self.project_id}/groups/{group_name}/hosts/{host_name}/vars",
            json=host_vars,
        )

    def make_validators_group_vars(self, subnet_id: str = "") -> dict:
        return {"subnet_id": subnet_id}

    def make_non_bootstraps_group_vars(
        self, bootstraps: str = "", resolver_bootstraps: str = ""
    ) -> dict:
        return {"bootstraps": bootstraps, "resolver_bootstraps": resolver_bootstraps}

    def populate_inventory(self) -> None:
        """Populate an Ansible inventory based on the configs provided"""
        hosts = self.merge_hosts_data()
        if len(hosts) == 0:
            logger.error("validators not found in configs")
            return

        # Create default groups
        for group_name in [
            self.GROUP_VALIDATORS,
            self.GROUP_BOOTSTRAPS,
            self.GROUP_NON_BOOTSTRAPS,
        ]:
            self.create_group(group_name=group_name)

        # Add all hosts to validators group
        for host in hosts:
            host_name = host["node"]["name"]
            self.add_host_to_group(
                group_name=self.GROUP_VALIDATORS,
                host_name=host_name,
            )

            # Additionaly populate host vars
            # TODO: Maybe sanitize it?
            node_name = host_name
            # TODO: Populate with actual role vars
            host_vars = {
                "ansible_host": host["conn"]["ipAddress"],
                "validator": {
                    "node_name": node_name,
                    "private_key_path": f"/home/ubuntu/.ipc/{node_name}.sk",
                    "cmt_p2p_host_port": "",
                    "cmt_rpc_host_port": "",
                    "ethapi_host_port": "",
                    "resolver_host_port": "",
                    "default_address": "",
                },
            }
            self.set_host_vars(
                group_name=self.GROUP_VALIDATORS,
                host_name=host_name,
                host_vars=host_vars,
            )

        # Pop one host from the list to use as a bootstrap
        bootstrap = hosts.pop()
        # Add the host to bootstraps group
        self.add_host_to_group(
            group_name=self.GROUP_BOOTSTRAPS,
            host_name=bootstrap["node"]["name"],
        )

        # Add the rest of the hosts as regular validators
        for host in hosts:
            self.add_host_to_group(
                group_name=self.GROUP_NON_BOOTSTRAPS,
                host_name=host["node"]["name"],
            )

    def run_prepare(self) -> str:
        params = {
            "extra_vars": {"var_host": self.GROUP_VALIDATORS},
            "tags": ["validator:prepare"],
        }
        logger.info(f"run prepare job: {params}")
        return self.run_validator_playbook(
            extra_vars=params["extra_vars"],
            tags=params["tags"],
        )

    def run_create_subnet(self) -> str:
        params = {
            "extra_vars": {"var_host": self.GROUP_BOOTSTRAPS},
            "tags": ["validator:create_subnet"],
        }
        logger.info(f"run create subnet job: {params}")
        return self.run_validator_playbook(
            extra_vars=params["extra_vars"],
            tags=params["tags"],
        )

    def run_join_subnet(self) -> str:
        params = {
            "extra_vars": {"var_host": self.GROUP_BOOTSTRAPS},
            "tags": ["validator:join_subnet"],
        }
        logger.info(f"run join subnet job: {params}")
        return self.run_validator_playbook(
            extra_vars=params["extra_vars"],
            tags=params["tags"],
        )

    def run_start_bootstrap(self) -> str:
        params = {
            "extra_vars": {"var_host": self.GROUP_BOOTSTRAPS},
            "tags": ["validator:start_bootstrap"],
        }
        logger.info(f"run start bootstrap job: {params}")
        return self.run_validator_playbook(
            extra_vars=params["extra_vars"],
            tags=params["tags"],
        )

    def run_start_validator(self) -> str:
        params = {
            "extra_vars": {"var_host": self.GROUP_NON_BOOTSTRAPS},
            "tags": ["validator:start"],
        }
        logger.info(f"run start validator job: {params}")
        return self.run_validator_playbook(
            extra_vars=params["extra_vars"],
            tags=params["tags"],
        )

    def run_start_relayer(self) -> str:
        params = {
            "extra_vars": {"var_host": self.GROUP_BOOTSTRAPS},
            "tags": ["validator:start_relayer"],
        }
        logger.info(f"run start relayer job: {params}")
        return self.run_validator_playbook(
            extra_vars=params["extra_vars"],
            tags=params["tags"],
        )

    def run_validator_playbook(self, extra_vars: dict = {}, tags: list = []) -> str:
        return self.run_playbook(
            playbook_name="validator.yaml",
            extra_vars=extra_vars,
            tags=tags,
        )

    def run_playbook(
        self, playbook_name: str, extra_vars: dict = {}, tags: list = []
    ) -> str:
        """Run specified playbook and return job_id

        Args:
            playbook_name (str): Name of the playbook to run.
            extra_vars (dict, optional): Extra vars to pass to the playbook. Defaults to {}.
            tags (list, optional): Tags to pass to the playbook. Defaults to [].

        Returns:
            str: ID of the running job.
        """
        payload = {"extra_vars": extra_vars, "tags": tags}

        res = self._request(
            method="POST",
            path=f"/playbooks/{playbook_name}/projects/{self.project_id}/run",
            json=payload,
        )

        res_json = res.json()

        return res_json["job_id"]

    def _request(self, method: str, path: str, json: dict = {}) -> requests.Response:
        """Wraper around the standard request method to apply the logging response hook.

        Args:
            method (str): HTTP method.
            path (str): HTTP path. Will be appended at the end of 'self.api_url'.
            json (dict, optional): JSON payload. Defaults to an empty dict.

        Returns:
            requests.Response: result of the operation
        """
        url = f"{self.api_url}{path}"
        return requests.request(
            method=method,
            url=url,
            json=json,
            hooks={"response": log_response_hook},
        )
