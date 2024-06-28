from app.exceptions import APIException


class PlaybooksAPIException(APIException):
    pass


class PlaybookNotFoundException(PlaybooksAPIException):
    code = 404
    description = "playbook_not_found"
