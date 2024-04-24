class KeysAPIException(Exception):
    pass


class NetworkNotConnectedException(KeysAPIException):
    code = 500
    description = "network_not_connected"


class NetworkNotFoundException(KeysAPIException):
    code = 500
    description = "network_not_found"
