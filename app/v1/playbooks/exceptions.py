class PlaybooksAPIException(Exception):
    pass


class PlaybookNotFoundException(PlaybooksAPIException):
    code = 404
    description = "playbook_not_found"
