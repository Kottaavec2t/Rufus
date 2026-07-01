class MessageException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

class PlayerNotFoundException(MessageException):
    def __init__(self, player: str):
        self.message = f'User **{player}** not found'
        super().__init__(self.message)

class InvalidInputException(MessageException):
    pass
