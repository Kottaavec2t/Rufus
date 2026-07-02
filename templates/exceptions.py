class MessageException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

class UserNotFoundException(MessageException):
    def __init__(self, username: str | None = None, id: int | str | None = None):
        if username: self.message = f'User **{username}** not found'
        elif id: self.message = f'Id **{id}** not found'
        super().__init__(self.message)

class LevelNotFoundException(MessageException):
    def __init__(self, level_id: int):
        self.message = f'Level **{level_id}** not found'
        super().__init__(self.message)

class PlaceNotFoundException(MessageException):
    def __init__(self, place_id: int):
        self.message = f'Place **{place_id}** not found'
        super().__init__(self.message)

class InvalidInputException(MessageException):
    pass
