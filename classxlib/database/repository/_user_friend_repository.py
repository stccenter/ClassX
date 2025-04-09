"""Database module for defining the UserFriendRepository Class"""

# Python Standard Library Imports
from typing import Any, List, Optional, Tuple

# Python Third Party Imports
from sqlalchemy import and_, or_, delete, select
from sqlalchemy.orm import Session, aliased

from classxlib.database.model._user import User

# Local Library Imports
from ..model import UserFriend
from ._base_repository import BaseRepository

__all__ = ["UserFriendRepository"]


class UserFriendRepository(BaseRepository):
    """The class for interacting/querying the `user_friends` SQL table.

    Args:
        session (Session): The database session object
            to use for querying and committing changes.
    """

    def __init__(self, session: Session):
        # Initializes the base repository class
        super().__init__(session=session, model=UserFriend, table_name="user_friends")

    def get_friend_row(self, sender_id: int, receiver_id: int) -> Optional[UserFriend]:
        """Gets a friend request status based on sender and receiver's user IDs.

        Args:
            sender_id (int): User ID of the first user to check against.
            receiver_id (int): User ID of the second user to check against.

        Returns:
            Optional[UserFriend]: The user friend database object, or None if not found.
        """
        stmt = select(UserFriend).where(
            or_(
                and_(
                    UserFriend.sender_id == sender_id,
                    UserFriend.receiver_id == receiver_id,
                ),
                and_(
                    UserFriend.sender_id == receiver_id,
                    UserFriend.receiver_id == sender_id,
                ),
            )
        )
        try:
            result = self.session.scalars(stmt).first()
            return result
        except Exception as e:
            print(f"Error fetching friend row between {sender_id} and {receiver_id}")
            print(e)
            return None

    def get_requests_by_status(
        self, sender_id: int, status: int, sender_only: bool = False
    ) -> List[Tuple[UserFriend, User, User]]:
        """Get all friend requests based on status.

        Args:
            sender_id (int): User ID who sent the requests.
            status (int): Status of the friend requests to filter by.
            sender_only (bool, optional): If True, filters only by sender ID. Defaults to False.

        Returns:
            List[Tuple[UserFriend, User, User]]: Pending requests with sender and receiver details.
        """
        sender_alias = aliased(User)
        receiver_alias = aliased(User)

        stmt = (
            select(UserFriend, sender_alias, receiver_alias)
            .join(sender_alias, UserFriend.sender_id == sender_alias.id)
            .join(receiver_alias, UserFriend.receiver_id == receiver_alias.id)
        )

        if sender_only:
            stmt = stmt.where(
                and_(
                    UserFriend.sender_id == sender_id,
                    UserFriend.status == status,
                )
            )
        else:
            stmt = stmt.where(
                and_(
                    UserFriend.status == status,
                    or_(
                        UserFriend.sender_id == sender_id,
                        UserFriend.receiver_id == sender_id,
                    ),
                )
            )

        try:
            results = self.session.execute(stmt).all()
            return results
        except Exception as e:
            print(
                f"Error fetching requests by status {status} for sender_id {sender_id}"
            )
            print(e)
            return []

    def update_status(
        self,
        sender_id: int,
        receiver_id: int,
        new_status: int,
        sender_only: bool = False,
    ) -> Optional[UserFriend]:
        """Updates the friend status between two users.

        Args:
            sender_id (int): User ID of the first user.
            receiver_id (int): User ID of the second user.
            new_status (int): New status to set.
            sender_only (bool, optional): If True, updates only where sender_id matches. Defaults to False.

        Returns:
            Optional[UserFriend]: Updated UserFriend object, or None if not found or update failed.
        """
        user_friend_obj = self.get_friend_row(sender_id, receiver_id)
        if user_friend_obj is None:
            return None

        user_friend_obj.status = new_status

        if not self.commit_changes():
            return None

        return user_friend_obj

    def remove_request(self, sender_id: int, receiver_id: int) -> bool:
        """Deletes a friend request between two users.

        Args:
            sender_id (int): User ID of the first user.
            receiver_id (int): User ID of the second user.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        stmt = delete(UserFriend).where(
            or_(
                and_(
                    UserFriend.sender_id == sender_id,
                    UserFriend.receiver_id == receiver_id,
                ),
                and_(
                    UserFriend.sender_id == receiver_id,
                    UserFriend.receiver_id == sender_id,
                ),
            )
        )
        try:
            self.session.execute(stmt)
            return self.commit_changes()
        except Exception as e:
            print(
                f"Error deleting friend request between {sender_id} and {receiver_id}"
            )
            print(e)
            return False
