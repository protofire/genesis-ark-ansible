class JobsAPIException(Exception):
    pass


class ArtifactsNotFound:
    code = 404
    description = "artifacts_not_found"
