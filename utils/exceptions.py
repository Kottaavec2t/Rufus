class MessageException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return self.message

class PlayerNotFoundException(MessageException):
    pass

class InvalidInputException(MessageException):
    pass