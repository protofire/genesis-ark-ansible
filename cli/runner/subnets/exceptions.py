from runner.exceptions import RunnerException


class SubnetManagerException(RunnerException):
    pass


class InstanceConnectionConfigNotFoundException(SubnetManagerException):
    pass


class WalletNotFoundException(SubnetManagerException):
    pass


class BootstrapsNotFound(SubnetManagerException):
    pass


class SubnetCreationEventNotFoundException(SubnetManagerException):
    pass


class SubnetIdNotFoundException(SubnetManagerException):
    pass


class BootstrapNodeStartEventNotFoundException(SubnetManagerException):
    pass


class CometBftNodeIdNotFoundException(SubnetManagerException):
    pass


class IpldResolverMultiaddressNotFoundException(SubnetManagerException):
    pass
