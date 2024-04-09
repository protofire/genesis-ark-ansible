class JobsAPIException(Exception):
    pass


class StatsNotFoundException(JobsAPIException):
    code = 404
    description = "stats_not_found"
