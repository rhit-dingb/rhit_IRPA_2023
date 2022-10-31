class NoDataFoundException(Exception):
    """Exception when no data is found given year or intent

    Attributes:
        message -- fallback message to tell the user
        exceptionType -- more specific type of the error
    """

    def __init__(self, fallBackMessage, exceptionType):
        self.type = exceptionType
        self.fallBackMessage = fallBackMessage
        super().__init__(self.fallBackMessage)