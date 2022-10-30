class EntityValueException(Exception):
    """Exception when entity value being processed is not what is expected. 

    Attributes:
        message -- fallback message to tell the user
        exceptionType -- more specific type of the error
    """

    def __init__(self, fallBackMessage, exceptionType):
        self.type = exceptionType
        self.fallBackMessage = fallBackMessage
        super().__init__(self.fallBackMessage)