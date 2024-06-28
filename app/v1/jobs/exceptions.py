from app.exceptions import APIException


class JobsAPIException(APIException):
    pass


class StatsNotFoundException(JobsAPIException):
    code = 404
    description = "stats_not_found"


class StatusNotFoundException(JobsAPIException):
    code = 404
    description = "status_not_found"
