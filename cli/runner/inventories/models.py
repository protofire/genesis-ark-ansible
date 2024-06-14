from runner.client import Client, safe
from runner.inventories.exceptions import (
    InventoriesClientException,
    GroupExistsException,
    GroupNotFoundException,
    GroupVarNotFoundException,
    HostExistsException,
    HostNotFoundException,
    HostNotFoundInGroupException,
    HostVarNotFoundException,
)
from runner.logging import logger


def exception_raiser(error_description: str, error_message: str) -> None:
    match error_description:
        case "group_not_found":
            raise GroupNotFoundException(error_message)
        case "group_exists":
            raise GroupExistsException(error_message)
        case "group_var_not_found":
            raise GroupVarNotFoundException(error_message)
        case "host_exists":
            raise HostExistsException(error_message)
        case "host_not_found_in_group":
            raise HostNotFoundInGroupException(error_message)
        case "host_not_found":
            raise HostNotFoundException(error_message)
        case "host_var_not_found":
            raise HostVarNotFoundException(error_message)
        case _:
            raise InventoriesClientException(error_message)


class InvenentoriesClient(Client):
    @safe(
        exception_raiser=exception_raiser, default_exception=InventoriesClientException
    )
    def list_groups(self, project_id: str) -> dict:
        logger.info(f"list groups in inventory of project '{project_id}'")
        return self.request(method="GET", path=f"/inventories/{project_id}/groups")

    @safe(
        exception_raiser=exception_raiser, default_exception=InventoriesClientException
    )
    def list_group_hosts(self, project_id: str, group_name: str) -> dict:
        logger.info(
            f"list hosts in group '{group_name}' in inventory of project '{project_id}'"
        )
        return self.request(
            method="GET", path=f"/inventories/{project_id}/groups/{group_name}/hosts"
        )

    @safe(
        exception_raiser=exception_raiser, default_exception=InventoriesClientException
    )
    def add_group(self, project_id: str, group_name: str) -> dict:
        logger.info(f"add group '{group_name}' in inventory of project '{project_id}'")
        return self.request(
            method="POST", path=f"/inventories/{project_id}/groups/{group_name}"
        )

    @safe(
        exception_raiser=exception_raiser, default_exception=InventoriesClientException
    )
    def del_group(self, project_id: str, group_name: str) -> dict:
        logger.info(
            f"delete group '{group_name}' from inventory of project '{project_id}'"
        )
        return self.request(
            method="DELETE", path=f"/inventories/{project_id}/groups/{group_name}"
        )

    @safe(
        exception_raiser=exception_raiser, default_exception=InventoriesClientException
    )
    def list_hosts(self, project_id: str) -> dict:
        logger.info(f"list hosts in inventory of project '{project_id}'")
        return self.request(method="GET", path=f"/inventories/{project_id}/hosts")

    @safe(
        exception_raiser=exception_raiser, default_exception=InventoriesClientException
    )
    def list_host_groups(self, project_id: str, host_name: str) -> dict:
        logger.info(
            f"list groups of host '{host_name}' in inventory of project '{project_id}'"
        )
        return self.request(
            method="GET", path=f"/inventories/{project_id}/hosts/{host_name}/groups"
        )

    @safe(
        exception_raiser=exception_raiser, default_exception=InventoriesClientException
    )
    def del_host(self, project_id: str, host_name: str) -> dict:
        logger.info(
            f"delete host '{host_name}' from inventory of project '{project_id}'"
        )
        return self.request(
            method="DELETE", path=f"/inventories/{project_id}/hosts/{host_name}"
        )

    @safe(
        exception_raiser=exception_raiser, default_exception=InventoriesClientException
    )
    def add_host_to_group(
        self, project_id: str, host_name: str, group_name: str
    ) -> dict:
        logger.info(
            f"add host '{host_name}' to group '{group_name}' in inventory of project '{project_id}'"
        )
        return self.request(
            method="POST",
            path=f"/inventories/{project_id}/hosts/{host_name}/groups/{group_name}",
        )

    @safe(
        exception_raiser=exception_raiser, default_exception=InventoriesClientException
    )
    def del_host_from_group(
        self, project_id: str, host_name: str, group_name: str
    ) -> dict:
        logger.info(
            f"delete host '{host_name}' from group '{group_name}' in inventory of project '{project_id}'"
        )
        return self.request(
            method="DELETE",
            path=f"/inventories/{project_id}/hosts/{host_name}/groups/{group_name}",
        )

    @safe(
        exception_raiser=exception_raiser, default_exception=InventoriesClientException
    )
    def list_host_vars(self, project_id: str, host_name: str, group_name: str) -> dict:
        logger.info(
            f"list host vars of host '{host_name}' in group '{group_name}' in inventory of project '{project_id}'"
        )
        return self.request(
            method="GET",
            path=f"/inventories/{project_id}/groups/{group_name}/hosts/{host_name}/vars",
        )

    @safe(
        exception_raiser=exception_raiser, default_exception=InventoriesClientException
    )
    def del_host_vars(self, project_id: str, host_name: str, group_name: str) -> dict:
        logger.log(
            f"delete host vars of host '{host_name}' in group '{group_name}' in inventory of project '{project_id}'"
        )
        return self.request(
            method="DELETE",
            path=f"/inventories/{project_id}/groups/{group_name}/hosts/{host_name}/vars",
        )

    @safe(
        exception_raiser=exception_raiser, default_exception=InventoriesClientException
    )
    def set_host_vars(
        self, project_id: str, host_name: str, group_name: str, host_vars: dict
    ) -> dict:
        logger.info(
            f"set host vars of host '{host_name}' in group '{group_name}' in inventory of project '{project_id}'"
        )
        return self.request(
            method="POST",
            path=f"/inventories/{project_id}/groups/{group_name}/hosts/{host_name}/vars",
            json=host_vars,
        )

    @safe(
        exception_raiser=exception_raiser, default_exception=InventoriesClientException
    )
    def list_group_vars(self, project_id: str, group_name: str) -> dict:
        logger.info(
            f"list group vars of group '{group_name}' in inventory of project '{project_id}'"
        )
        return self.request(
            method="GET",
            path=f"/inventories/{project_id}/groups/{group_name}/vars",
        )

    @safe(
        exception_raiser=exception_raiser, default_exception=InventoriesClientException
    )
    def del_group_vars(self, project_id: str, group_name: str) -> dict:
        logger.info(
            f"delete group vars of group '{group_name}' in inventory of project '{project_id}'"
        )
        return self.request(
            method="DELETE",
            path=f"/inventories/{project_id}/groups/{group_name}/vars",
        )

    @safe(
        exception_raiser=exception_raiser, default_exception=InventoriesClientException
    )
    def set_group_vars(
        self, project_id: str, group_name: str, group_vars: dict
    ) -> dict:
        logger.info(
            f"set group vars of group '{group_name}' in inventory of project '{project_id}'"
        )
        return self.request(
            method="POST",
            path=f"/inventories/{project_id}/groups/{group_name}/vars",
            json=group_vars,
        )
