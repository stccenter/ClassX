"""The pythonic dataclass for the user_levels table"""
# Python Standard Library Imports
from dataclasses import dataclass

# Local Library Imports
from ._base import BaseModel

__all__ = ['UserFriend']

@dataclass(unsafe_hash=True)
class UserFriend(BaseModel): # pylint: disable=too-many-instance-attributes
    """The dataclass that is the pythonic representation of
    a single row in the `user_friends` sql database table.
    Each attribute of the class is a column in the sql table.
    Attributes:
        id (`int`, `primary-key`, `auto-increment`):
        The id associated with the user_friends.
        sender_id (`int`): The request sender/initiator of the status action
        e.g. you send "chicken" a friend request.
        receiver_id (`int`): The request sender/initiator of the status action
        e.g. "chicken" sent you a friend request.
        status (`int`): Status of the request (Pending, Accepted, Denied, Blocked)
        e.g. You accept "chicken"'s friend request so the status is no longer 0 

    """
    # NOTE for descriptions on the class attributes refer
    # to the docstring
    id : int
    sender_id : int
    receiver_id : int
    status : int

    # Initialize the attributes
    # pylint: disable=too-many-arguments, too-many-locals
    def __init__(self, sender_id, receiver_id,
                 status):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.status = status
