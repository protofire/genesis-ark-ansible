import re

from runner.inventories.exceptions import GroupExistsException, HostExistsException
from runner.inventories.models import InvenentoriesClient
from runner.jobs.models import JobsClient
from runner.keys.models import KeysClient
from runner.logging import logger
from runner.playbooks.models import PlaybooksClient
from runner.subnets.exceptions import (
    BootstrapsNotFound,
    InstanceConnectionConfigNotFoundException,
    SubnetCreationEventNotFoundException,
    SubnetIdNotFoundException,
    WalletNotFoundException,
    BootstrapNodeStartEventNotFoundException,
    CometBftNodeIdNotFoundException,
    IpldResolverMultiaddressNotFoundException,
)


class AnsibleOperator:
    BOOTSTRAPS_GROUP_NAME = "bootstraps"
    NON_BOOTSTRAPS_GROUP_NAME = "non_bootstraps"
    VALIDATORS_GROUP_NAME = "validators"
    CONTOL_GROUP_NAME = "control"

    def __init__(self, subnet_config: dict, conn_config: dict) -> None:
        # set incoming configs
        self.subnet_config = subnet_config
        self.conn_config = conn_config

        # compute and set project id
        self.project_id = self.get_project_id()

        # set contextualized logger
        self.logger = logger.bind(project_id=self.project_id)

        # set API clients with contextualized loggers
        self.keys_client = KeysClient(logger=self.logger)
        self.inventories_client = InvenentoriesClient(logger=self.logger)
        self.playbooks_client = PlaybooksClient(logger=self.logger)
        self.jobs_client = JobsClient(logger=self.logger)

        # set miscellanious computed facts
        self.secrets = self.compute_secrets()
        self.bootstraps = self.get_bootstrap_validators_node_configs()

    def get_project_id(self) -> str:
        return self.subnet_config["id"]

    def compute_wallet_details(self, validator_name: str, private_key: str) -> dict:
        public_key_res = self.keys_client.get_public_key(private_key=private_key)
        address_res = self.keys_client.get_address(
            private_key=private_key, network_type_for="prod"
        )
        return {
            "name": validator_name,
            "address": address_res["address"],
            "public_key": public_key_res["publicKey"],
            "private_key": private_key,
        }

    def is_validator(self, node_config: dict) -> bool:
        node_config_keys = node_config.keys()
        return "PrivateKey" in node_config_keys and "stake" in node_config_keys

    def compute_secrets(self) -> dict:
        secrets = {"wallets": []}
        for node_config in self.subnet_config["nodes"]:
            if not self.is_validator(node_config=node_config):
                continue
            secrets["wallets"].append(
                self.compute_wallet_details(
                    validator_name=self.get_validator_name(node_config=node_config),
                    private_key=node_config["PrivateKey"],
                )
            )
        return secrets

    def prepare(self):
        res = self.playbooks_client.prepare(
            project_id=self.project_id,
            extra_vars={"var_host": self.VALIDATORS_GROUP_NAME},
        )

        return res["job_id"]

    def create_subnet(self) -> str:
        res = self.playbooks_client.create_subnet(
            project_id=self.project_id,
            extra_vars={"var_host": self.CONTOL_GROUP_NAME},
        )

        return res["job_id"]

    def get_cometbft_node_id(self, job_id: str) -> str:
        events_res = self.jobs_client.list_events(
            job_id=job_id,
            events_filter={
                "event": "runner_on_ok",
                "task": "Print run bootstrap command output",
            },
        )

        if len(events_res) != 1:
            raise BootstrapNodeStartEventNotFoundException(
                "bootstrap start event not found", job_id=job_id
            )

        bootstrap_started_event = events_res[0]
        stdout = bootstrap_started_event["event_data"]["res"]["msg"]["stdout"]

        pattern = r"CometBFT node ID:\s+([a-z0-9]+)"
        found = re.findall(pattern=pattern, string=stdout)
        if len(found) == 0:
            raise CometBftNodeIdNotFoundException(
                "cometbft node id not found in event stdout",
                job_id=job_id,
                event_uuid=bootstrap_started_event["uuid"],
            )

        return found[0]

    def set_validator_bootstraps(
        self, cometbft_node_id: str, ip_address: str, port: int = 26656
    ) -> None:
        validator_bootstraps = f"{cometbft_node_id}@{ip_address}:{port}"
        self.inventories_client.set_group_vars(
            project_id=self.project_id,
            group_name=self.NON_BOOTSTRAPS_GROUP_NAME,
            group_vars={"validator_bootstraps": validator_bootstraps},
        )

    def get_ipld_resolver_multiaddress(self, job_id: str) -> str:
        events_res = self.jobs_client.list_events(
            job_id=job_id,
            events_filter={
                "event": "runner_on_ok",
                "task": "Print run bootstrap command output",
            },
        )

        if len(events_res) != 1:
            raise BootstrapNodeStartEventNotFoundException(
                "bootstrap start event not found", job_id=job_id
            )

        bootstrap_started_event = events_res[0]
        stdout = bootstrap_started_event["event_data"]["res"]["msg"]["stdout"]
        pattern = r"IPLD Resolver Multiaddress:\s+([A-z0-9\/\.]+)"
        found = re.findall(pattern=pattern, string=stdout)
        if len(found) == 0:
            raise IpldResolverMultiaddressNotFoundException(
                "ipld resolver multiaddr not found in event stdout",
                job_id=job_id,
                event_uuid=bootstrap_started_event["uuid"],
            )

        return found[0]

    def set_validator_resolver_bootstraps(
        self, multiaddr: str, ip_address: str
    ) -> None:
        validator_resolver_bootstraps = multiaddr.replace("0.0.0.0", ip_address)
        self.inventories_client.set_group_vars(
            project_id=self.project_id,
            group_name=self.NON_BOOTSTRAPS_GROUP_NAME,
            group_vars={"validator_resolver_bootstraps": validator_resolver_bootstraps},
        )

    def get_subnet_id(self, job_id: str) -> str:
        event_type = "runner_on_ok"
        task_name = "Print create subnet output"

        events = self.jobs_client.list_events(
            job_id=job_id,
            events_filter={
                "event": event_type,
                "task": task_name,
            },
        )

        if len(events) != 1:
            raise SubnetCreationEventNotFoundException(
                "subnet creation event not found", job_id=job_id
            )

        event = events[0]

        pattern = r".*created subnet actor with id: ([\/a-z0-9]+)"
        found = re.findall(
            pattern=pattern, string=event["event_data"]["res"]["msg"]["stdout"]
        )

        if len(found) == 0:
            raise SubnetIdNotFoundException(
                "subnet id not found in event stdout",
                job_id=job_id,
                event_uuid=event["uuid"],
            )

        full_subnet_id = found[0]
        chunks = full_subnet_id.split("/")

        return chunks[-1]

    def copy_config(self) -> str:
        res = self.playbooks_client.copy_config(
            project_id=self.project_id,
            extra_vars={"var_host": self.VALIDATORS_GROUP_NAME},
        )

        return res["job_id"]

    def start_bootstrap(self) -> str:
        res = self.playbooks_client.start_bootstrap(
            project_id=self.project_id,
            extra_vars={"var_host": self.BOOTSTRAPS_GROUP_NAME},
        )

        return res["job_id"]

    def start_validators(self) -> str:
        res = self.playbooks_client.start_validator(
            project_id=self.project_id,
            extra_vars={"var_host": self.NON_BOOTSTRAPS_GROUP_NAME},
        )

        return res["job_id"]

    def start_relayer(self) -> str:
        res = self.playbooks_client.start_relayer(
            project_id=self.project_id,
            extra_vars={"var_host": self.BOOTSTRAPS_GROUP_NAME},
        )

        return res["job_id"]

    def get_instance_connection_config(self, node_id: int) -> dict:
        for instance_connection_config in self.conn_config["instanceconnections"]:
            if instance_connection_config["nodeId"] == node_id:
                return instance_connection_config
        raise InstanceConnectionConfigNotFoundException(
            f"instance connection config not found for node '{node_id}'"
        )

    def get_validator_name(self, node_config: dict) -> str:
        return node_config["name"]

    def get_validator_wallet(self, validator_name: str) -> dict:
        for wallet in self.secrets["wallets"]:
            if wallet["name"] == validator_name:
                return wallet
        raise WalletNotFoundException(
            f"wallet details for validator '{validator_name}' not found in secrets"
        )

    def get_validator_default_address(self, validator_name: str) -> str:
        wallet = self.get_validator_wallet(validator_name=validator_name)
        return wallet["address"]

    def set_subnet_id(self, subnet_id: str) -> None:
        self.inventories_client.set_group_vars(
            project_id=self.project_id,
            group_name=self.VALIDATORS_GROUP_NAME,
            group_vars={"validator_subnet_id": subnet_id},
        )

    def join_subnet(self) -> str:
        res = self.playbooks_client.join_subnet(
            project_id=self.project_id,
            extra_vars={"var_host": self.CONTOL_GROUP_NAME},
        )

        return res["job_id"]

    def get_bootstrap_ip_address(self) -> str:
        connection_config = self.get_instance_connection_config(
            node_id=self.bootstraps[0]["id"]
        )

        return connection_config["ipAddress"]

    def compute_host_vars(self, node_config: dict) -> dict:
        instance_connection_config = self.get_instance_connection_config(
            node_id=node_config["id"]
        )
        validator_name = self.get_validator_name(node_config=node_config)
        return {
            "ansible_host": instance_connection_config["ipAddress"],
            "validator_name": validator_name,
            "validator_private_key_path": f"/home/ubuntu/.ipc/{validator_name}.sk",
            "validator_parent_subnet_id": "r314159",
            "validator_parent_registry": "0xc938B2B862d4Ef9896E641b3f1269DabFB2D2103",
            "validator_parent_gateway": "0x6d25fbFac9e6215E03C687E54F7c74f489949EaF",
            "validator_min_validator_stake": self.subnet_config["minStake"],
            "validator_min_validators": 1,
            "validator_bottom_check_period": self.subnet_config["bottomUp"],
            "validator_permission_mode": "collateral",
            "validator_supply_source_kind": "native",
            "validator_default_address": self.get_validator_default_address(
                validator_name=validator_name
            ),
            "validator_secrets": self.secrets,
            "ansible_sudo_pass": "12345",  # TODO: replace with the sudo password of the host somehow
        }

    def get_bootstrap_validators_node_configs(self) -> list[dict]:
        bootstrap_validators_node_configs = []
        for node_config in self.subnet_config["nodes"]:
            # TODO: come up with more sensible criteria for electing bootstrap nodes
            if self.is_validator(node_config=node_config):
                bootstrap_validators_node_configs.append(node_config)
                return bootstrap_validators_node_configs
        raise BootstrapsNotFound("couldn't elect bootstraps among validators")

    def get_control_node_config(self) -> dict:
        # TODO: come up with more sensible criteria for electing control node
        return self.bootstraps[0]

    def create_inventory(self) -> dict:
        # Create control group in the inventory.
        try:
            self.inventories_client.add_group(
                project_id=self.project_id, group_name=self.CONTOL_GROUP_NAME
            )
        except GroupExistsException as e:
            logger.warning(e.args[0], **e.extra)

        control_node_config = self.get_control_node_config()
        control_node_host_name = self.get_validator_name(
            node_config=control_node_config
        )

        try:
            self.inventories_client.add_host_to_group(
                project_id=self.project_id,
                host_name=control_node_host_name,
                group_name=self.CONTOL_GROUP_NAME,
            )
        except HostExistsException as e:
            logger.warning(e.args[0], **e.extra)

        control_host_vars = self.compute_host_vars(node_config=control_node_config)
        self.inventories_client.set_host_vars(
            project_id=self.project_id,
            host_name=control_node_host_name,
            group_name=self.CONTOL_GROUP_NAME,
            host_vars=control_host_vars,
        )

        # Create bootstraps group in the inventory.
        try:
            self.inventories_client.add_group(
                project_id=self.project_id, group_name=self.BOOTSTRAPS_GROUP_NAME
            )
        except GroupExistsException as e:
            logger.warning(e.args[0], **e.extra)

        # Add bootstrap hosts to bootstrap group and set host vars
        for node_config in self.bootstraps:
            host_name = self.get_validator_name(node_config=node_config)
            try:
                self.inventories_client.add_host_to_group(
                    project_id=self.project_id,
                    host_name=host_name,
                    group_name=self.BOOTSTRAPS_GROUP_NAME,
                )
            except HostExistsException as e:
                logger.warning(e.args[0], **e.extra)

            host_vars = self.compute_host_vars(node_config=node_config)
            self.inventories_client.set_host_vars(
                project_id=self.project_id,
                host_name=host_name,
                group_name=self.BOOTSTRAPS_GROUP_NAME,
                host_vars=host_vars,
            )

        # Create non-bootstraps group in the inventory.
        try:
            self.inventories_client.add_group(
                project_id=self.project_id, group_name="non_bootstraps"
            )
        except GroupExistsException as e:
            logger.warning(e.args[0], **e.extra)

        # Create validators group in the inventory. This group includes both bootstrap and non-bootstrap nodes
        try:
            self.inventories_client.add_group(
                project_id=self.project_id, group_name="validators"
            )
        except GroupExistsException as e:
            logger.warning(e.args[0], **e.extra)

        # Add validators to the validator group and set host vars
        # Add non-bootstrap nodes to the non_bootstraps group and set host vars
        for node_config in self.subnet_config["nodes"]:
            # Skip non-validator nodes
            if not self.is_validator(node_config=node_config):
                continue

            host_name = self.get_validator_name(node_config=node_config)
            try:
                self.inventories_client.add_host_to_group(
                    project_id=self.project_id,
                    host_name=host_name,
                    group_name=self.VALIDATORS_GROUP_NAME,
                )
            except HostExistsException as e:
                logger.warning(e.args[0], **e.extra)

            host_vars = self.compute_host_vars(node_config=node_config)
            self.inventories_client.set_host_vars(
                project_id=self.project_id,
                host_name=host_name,
                group_name=self.VALIDATORS_GROUP_NAME,
                host_vars=host_vars,
            )

            # skip nodes present in bootstraps list
            if node_config["id"] in [
                bootstrap_node_config["id"] for bootstrap_node_config in self.bootstraps
            ]:
                continue

            try:
                self.inventories_client.add_host_to_group(
                    project_id=self.project_id,
                    host_name=host_name,
                    group_name=self.NON_BOOTSTRAPS_GROUP_NAME,
                )
            except HostExistsException as e:
                logger.warning(e.args[0], **e.extra)

            self.inventories_client.set_host_vars(
                project_id=self.project_id,
                host_name=host_name,
                group_name=self.NON_BOOTSTRAPS_GROUP_NAME,
                host_vars=host_vars,
            )
