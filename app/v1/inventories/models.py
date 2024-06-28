import os

import yaml
from flask import current_app

from app.v1.inventories.exceptions import (
    GroupExistsException,
    GroupNotFoundException,
    GroupVarNotFoundException,
    HostExistsException,
    HostNotFoundException,
    HostNotFoundInGroupException,
    HostVarNotFoundException,
)


class Inventory:
    """
    Represents the file <project_id>.yaml.
    The file is located in the inventories directory.
    """

    def __init__(self, project_id: str) -> None:
        self.project_id = project_id

        inventories_dir = current_app.config["INVENTORIES_DIR"]
        self.inventory_path = os.path.join(inventories_dir, f"{project_id}.yaml")
        self.inventory = None

    def load(self) -> None:
        """
        Loads inventory file as dict.
        Stores it in `self.inventory`.
        If file not found, stores empty inventory.
        """
        if not os.path.exists(self.inventory_path):
            self.inventory = {"all": {"children": {}}}
        else:
            with open(self.inventory_path, "r") as f:
                self.inventory = yaml.safe_load(f)

    def dump(self) -> str:
        """
        Dumps inventory as yaml.

        Returns:
            str: yaml encoded inventory
        """
        return yaml.safe_dump(data=self.inventory)

    def save(self) -> None:
        """
        Dumps inventory as yaml.
        Saves result to inventory file.
        """
        with open(self.inventory_path, "w") as f:
            yaml.safe_dump(data=self.inventory, stream=f)

    def is_loaded(self) -> bool:
        return self.inventory is not None

    def get_groups(self) -> dict:
        return self.inventory["all"]["children"]

    def list_group_names(self) -> list[str]:
        return list(self.get_groups().keys())

    def is_group_exists(self, group_name: str) -> bool:
        return group_name in self.list_group_names()

    def get_group(self, group_name: str) -> dict:
        if not self.is_group_exists(group_name=group_name):
            raise GroupNotFoundException(
                "failed to get group: group not found",
                group_name=group_name,
                project_id=self.project_id,
            )
        return self.inventory["all"]["children"][group_name]

    def get_group_vars(self, group_name: str) -> dict:
        return self.get_group(group_name=group_name)["vars"]

    def list_group_vars_names(self, group_name: str) -> list[str]:
        return sorted(list(self.get_group(group_name=group_name)["vars"].keys()))

    def is_group_var_exists(self, group_name: str, var_name: str) -> bool:
        return var_name in self.list_group_vars_names(group_name=group_name)

    def get_group_hosts(self, group_name: str) -> dict:
        return self.get_group(group_name=group_name)["hosts"]

    def list_group_hosts_names(self, group_name: str) -> list[str]:
        return sorted(list(self.get_group(group_name=group_name)["hosts"].keys()))

    def add_group(self, group_name: str) -> None:
        if self.is_group_exists(group_name=group_name):
            raise GroupExistsException(
                "failed to add group: group already exists",
                group_name=group_name,
                project_id=self.project_id,
            )
        self.inventory["all"]["children"][group_name] = {"hosts": {}, "vars": {}}

    def delete_group(self, group_name: str) -> None:
        if not self.is_group_exists(group_name=group_name):
            raise GroupNotFoundException(
                "failed to delete group: group not found",
                group_name=group_name,
                project_id=self.project_id,
            )
        del self.inventory["all"]["children"][group_name]

    def set_group_var(self, group_name: str, var_name: str, var_value) -> None:
        if not self.is_group_exists(group_name=group_name):
            raise GroupNotFoundException(
                "failed to set group var: group not found",
                group_name=group_name,
                project_id=self.project_id,
            )
        self.inventory["all"]["children"][group_name]["vars"][var_name] = var_value

    def set_group_vars(self, group_name: str, group_vars: dict) -> None:
        if not self.is_group_exists(group_name=group_name):
            raise GroupNotFoundException(
                "failed to set group vars: group not found",
                group_name=group_name,
                project_id=self.project_id,
            )
        self.inventory["all"]["children"][group_name]["vars"] = group_vars

    def delete_group_var(self, group_name: str, var_name: str) -> None:
        if not self.is_group_var_exists(group_name=group_name, var_name=var_name):
            raise GroupVarNotFoundException(
                "failed to unset group var: var not found in group",
                var_name=var_name,
                group_name=group_name,
                project_id=self.project_id,
            )
        del self.inventory["all"]["children"][group_name]["vars"][var_name]

    def delete_group_vars(self, group_name: str) -> None:
        if not self.is_group_exists(group_name=group_name):
            raise GroupNotFoundException(
                "failed to unset group vars: group not found",
                group_name=group_name,
                project_id=self.project_id,
            )
        self.inventory["all"]["children"][group_name]["vars"] = {}

    def is_group_host_exists(self, group_name: str, host_name: str) -> bool:
        return host_name in self.list_group_hosts_names(group_name=group_name)

    def add_group_host(self, group_name: str, host_name: str) -> None:
        if self.is_group_host_exists(group_name=group_name, host_name=host_name):
            raise HostExistsException(
                "failed to add host to group: host already exists in group",
                host_name=host_name,
                group_name=group_name,
                project_id=self.project_id,
            )
        self.inventory["all"]["children"][group_name]["hosts"][host_name] = {}

    def delete_group_host(self, group_name: str, host_name: str) -> None:
        if not self.is_group_host_exists(group_name=group_name, host_name=host_name):
            raise HostNotFoundInGroupException(
                "failed to delete host from group: host not found in group",
                host_name=host_name,
                group_name=group_name,
                project_id=self.project_id,
            )
        del self.inventory["all"]["children"][group_name]["hosts"][host_name]

    def get_group_host_vars(self, group_name: str, host_name: str) -> dict:
        if not self.is_group_host_exists(group_name=group_name, host_name=host_name):
            raise HostNotFoundInGroupException(
                "failed to get host vars: host not found in group",
                host_name=host_name,
                group_name=group_name,
                project_id=self.project_id,
            )
        return self.inventory["all"]["children"][group_name]["hosts"][host_name]

    def list_group_host_vars_names(self, group_name: str, host_name: str) -> list[str]:
        return sorted(
            self.get_group_host_vars(group_name=group_name, host_name=host_name).keys()
        )

    def is_group_host_var_exists(
        self, group_name: str, host_name: str, var_name: str
    ) -> bool:
        return var_name in self.list_group_host_vars_names(
            group_name=group_name, host_name=host_name
        )

    def set_group_host_var(
        self, group_name: str, host_name: str, var_name: str, var_value
    ) -> None:
        if not self.is_group_host_exists(group_name=group_name, host_name=host_name):
            raise HostNotFoundInGroupException(
                "failed to set host var: host not found in group",
                var_name=var_name,
                var_value=var_value,
                host_name=host_name,
                group_name=group_name,
                project_id=self.project_id,
            )
        self.inventory["all"]["children"][group_name]["hosts"][host_name][var_name] = (
            var_value
        )

    def delete_group_host_var(
        self, group_name: str, host_name: str, var_name: str
    ) -> None:
        if not self.is_group_host_var_exists(
            group_name=group_name, host_name=host_name, var_name=var_name
        ):
            raise HostVarNotFoundException(
                "failed to unset host var: host var not found",
                var_name=var_name,
                host_name=host_name,
                group_name=group_name,
                project_id=self.project_id,
            )
        del self.inventory["all"]["children"][group_name]["hosts"][host_name][var_name]

    def set_group_host_vars(
        self, group_name: str, host_name: str, host_vars: dict
    ) -> None:
        if not self.is_group_host_exists(group_name=group_name, host_name=host_name):
            raise HostNotFoundException(
                "failed to set host vars: host not found in group",
                host_vars=host_vars,
                host_name=host_name,
                group_name=group_name,
                project_id=self.project_id,
            )
        self.inventory["all"]["children"][group_name]["hosts"][host_name] = host_vars

    def delete_group_host_vars(self, group_name: str, host_name: str) -> None:
        if not self.is_group_host_exists(group_name=group_name, host_name=host_name):
            raise HostNotFoundException(
                "failed to unset host vars: host not found in group",
                host_name=host_name,
                group_name=group_name,
                project_id=self.project_id,
            )
        self.inventory["all"]["children"][group_name]["hosts"][host_name] = {}

    def list_host_names(self) -> list[str]:
        host_names = set()
        for group_name in self.list_group_names():
            for host_name in self.list_group_hosts_names(group_name=group_name):
                host_names.add(host_name)
        return sorted(list(host_names))

    def list_host_groups_names(self, host_name) -> list[str]:
        group_names = set()
        for group_name in self.list_group_names():
            if host_name in self.list_group_hosts_names(group_name=group_name):
                group_names.add(group_name)
        if len(group_names) == 0:
            raise HostNotFoundException(
                "failed to list host groups: host not found in any group",
                host_name=host_name,
                project_id=self.project_id,
            )
        return sorted(list(group_names))

    def delete_host(self, host_name) -> None:
        for group_name in self.list_group_names():
            self.delete_group_host(group_name=group_name, host_name=host_name)
