class InventoriesAPIException(Exception):
    pass


class GroupNotFoundException(InventoriesAPIException):
    code = 404
    description = "group_not_found"


class GroupExistsException(InventoriesAPIException):
    code = 500
    description = "group_exists"


class GroupVarNotFoundException(InventoriesAPIException):
    code = 404
    description = "group_var_not_found"


class HostExistsException(InventoriesAPIException):
    code = 500
    description = "host_exists"


class HostNotFoundInGroupException(InventoriesAPIException):
    code = 404
    description = "host_not_found_in_group"


class HostNotFoundException(InventoriesAPIException):
    code = 404
    description = "host_not_found"


class HostVarNotFoundException(InventoriesAPIException):
    code = 404
    description = "host_var_not_found"
