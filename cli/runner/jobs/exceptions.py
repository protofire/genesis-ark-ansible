from runner.exceptions import RunnerException


class JobsClientException(RunnerException):
    pass


class StatusNotFoundException(JobsClientException):
    pass


class StatsNotFoundException(JobsClientException):
    pass


class TimeoutWaitingForCompletionException(JobsClientException):
    pass
