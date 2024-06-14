from runner.exceptions import RunnerException


class InventoriesClientException(RunnerException):
    pass


class GroupNotFoundException(InventoriesClientException):
    pass


class GroupExistsException(InventoriesClientException):
    pass


class GroupVarNotFoundException(InventoriesClientException):
    pass


class HostExistsException(InventoriesClientException):
    pass


class HostNotFoundException(InventoriesClientException):
    pass


class HostNotFoundInGroupException(InventoriesClientException):
    pass


class HostVarNotFoundException(InventoriesClientException):
    pass
