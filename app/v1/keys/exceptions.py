from app.exceptions import APIException


class KeysAPIException(APIException):
    pass


class NetworkNotConnectedException(KeysAPIException):
    code = 500
    description = "network_not_connected"


class NetworkNotFoundException(KeysAPIException):
    code = 500
    description = "network_not_found"
