class NotEnoughInformationException(Exception):
    """Exception when an intent of the user is detected, but they did not specify any other information.

    Attributes:
        message -- fallback message to tell the user
        exceptionType -- more specific type of the error
    """

    def __init__(self, fallBackMessage, exceptionType):
        self.type = exceptionType
        self.fallBackMessage = fallBackMessage
        super().__init__(self.fallBackMessage)