from runner.exceptions import RunnerException


class SubnetManagerException(RunnerException):
    pass


class InstanceConnectionConfigNotFoundException(SubnetManagerException):
    pass


class WalletNotFoundException(SubnetManagerException):
    pass


class BootstrapsNotFound(SubnetManagerException):
    pass
