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


def exception_raiser(error: dict) -> None:
    match error["error"]:
        case "group_not_found":
            raise GroupNotFoundException(**error)
        case "group_exists":
            raise GroupExistsException(**error)
        case "group_var_not_found":
            raise GroupVarNotFoundException(**error)
        case "host_exists":
            raise HostExistsException(**error)
        case "host_not_found_in_group":
            raise HostNotFoundInGroupException(**error)
        case "host_not_found":
            raise HostNotFoundException(**error)
        case "host_var_not_found":
            raise HostVarNotFoundException(**error)
        case _:
            raise InventoriesClientException(**error)


class InvenentoriesClient(Client):
    LOGGER_NAME = "inventories"

    @safe(
        exception_raiser=exception_raiser, default_exception=InventoriesClientException
    )
    def list_groups(self, project_id: str) -> dict:
        self.logger.info("list groups", project_id=project_id)
        return self.request(method="GET", path=f"/inventories/{project_id}/groups")

    @safe(
        exception_raiser=exception_raiser, default_exception=InventoriesClientException
    )
    def list_group_hosts(self, project_id: str, group_name: str) -> dict:
        self.logger.info(
            "list group hosts", project_id=project_id, group_name=group_name
        )
        return self.request(
            method="GET", path=f"/inventories/{project_id}/groups/{group_name}/hosts"
        )

    @safe(
        exception_raiser=exception_raiser, default_exception=InventoriesClientException
    )
    def add_group(self, project_id: str, group_name: str) -> dict:
        self.logger.info("add group", project_id=project_id, group_name=group_name)
        return self.request(
            method="POST", path=f"/inventories/{project_id}/groups/{group_name}"
        )

    @safe(
        exception_raiser=exception_raiser, default_exception=InventoriesClientException
    )
    def del_group(self, project_id: str, group_name: str) -> dict:
        self.logger.info("delete group", project_id=project_id, group_name=group_name)
        return self.request(
            method="DELETE", path=f"/inventories/{project_id}/groups/{group_name}"
        )

    @safe(
        exception_raiser=exception_raiser, default_exception=InventoriesClientException
    )
    def list_hosts(self, project_id: str) -> dict:
        self.logger.info("list hosts in all groups", project_id=project_id)
        return self.request(method="GET", path=f"/inventories/{project_id}/hosts")

    @safe(
        exception_raiser=exception_raiser, default_exception=InventoriesClientException
    )
    def list_host_groups(self, project_id: str, host_name: str) -> dict:
        self.logger.info("list host groups", project_id=project_id, host_name=host_name)
        return self.request(
            method="GET", path=f"/inventories/{project_id}/hosts/{host_name}/groups"
        )

    @safe(
        exception_raiser=exception_raiser, default_exception=InventoriesClientException
    )
    def del_host(self, project_id: str, host_name: str) -> dict:
        self.logger.info(
            "delete host from all groups", project_id=project_id, host_name=host_name
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
        self.logger.info(
            "add host",
            project_id=project_id,
            group_name=group_name,
            host_name=host_name,
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
        self.logger.info(
            "delete host from group",
            project_id=project_id,
            group_name=group_name,
            host_name=host_name,
        )
        return self.request(
            method="DELETE",
            path=f"/inventories/{project_id}/hosts/{host_name}/groups/{group_name}",
        )

    @safe(
        exception_raiser=exception_raiser, default_exception=InventoriesClientException
    )
    def list_host_vars(self, project_id: str, host_name: str, group_name: str) -> dict:
        self.logger.info(
            "list host vars",
            project_id=project_id,
            group_name=group_name,
            host_name=host_name,
        )
        return self.request(
            method="GET",
            path=f"/inventories/{project_id}/groups/{group_name}/hosts/{host_name}/vars",
        )

    @safe(
        exception_raiser=exception_raiser, default_exception=InventoriesClientException
    )
    def del_host_vars(self, project_id: str, host_name: str, group_name: str) -> dict:
        self.logger.log(
            "delete host vars",
            project_id=project_id,
            group_name=group_name,
            host_name=host_name,
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
        self.logger.info(
            "set host vars",
            project_id=project_id,
            group_name=group_name,
            host_name=host_name,
            host_vars=host_vars,
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
        self.logger.info(
            "list group vars", project_id=project_id, group_name=group_name
        )
        return self.request(
            method="GET",
            path=f"/inventories/{project_id}/groups/{group_name}/vars",
        )

    @safe(
        exception_raiser=exception_raiser, default_exception=InventoriesClientException
    )
    def del_group_vars(self, project_id: str, group_name: str) -> dict:
        self.logger.info(
            "delete group vars", project_id=project_id, group_name=group_name
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
        self.logger.info(
            "set group vars",
            project_id=project_id,
            group_name=group_name,
            group_vars=group_vars,
        )
        return self.request(
            method="POST",
            path=f"/inventories/{project_id}/groups/{group_name}/vars",
            json=group_vars,
        )
