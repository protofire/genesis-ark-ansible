class APIException(Exception):
    def __init__(self, message, **kwargs):
        self.extra = kwargs
        super().__init__(message)
