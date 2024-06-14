from runner.exceptions import RunnerException


class KeysClientException(RunnerException):
    pass


class NetworkNotConnectedException(KeysClientException):
    pass


class NetworkNotFoundException(KeysClientException):
    pass
