from typing import Any


class BoulderBuddyException(Exception):
    pass


class NotFoundException(BoulderBuddyException):
    pass


class AlreadyExistsException(BoulderBuddyException):
    def __init__(self, message: str, resource_id: Any, *args: object) -> None:
        self.message = message
        self.resource_id = resource_id
        super().__init__(*args)
