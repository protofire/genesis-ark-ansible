from runner.exceptions import RunnerException


class PlaybooksClientException(RunnerException):
    pass


class PlaybookNotFoundException(PlaybooksClientException):
    pass
