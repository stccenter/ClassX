"""Database module for defining the UserResearchFieldRepository Class"""

# Python Third Party Imports
from typing import Any, Dict, List, Optional

from sqlalchemy import and_, delete, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Local Library Imports
from ..model import UserResearchField
from ._base_repository import BaseRepository

__all__ = ["UserResearchFieldRepository"]


class UserResearchFieldRepository(BaseRepository):
    """The class for interacting/querying the `user_friends` sql table.
    Args:
        session(sqlalchemy.orm.Session): The database session object
        to use for querying and commiting changes.
    """

    def __init__(self, session: Session):
        # Initializes the base repository class
        super().__init__(
            session=session, model=UserResearchField, table_name="user_research_fields"
        )

    def get_research_ids(self, user_id: int) -> List[UserResearchField]:
        """Gets all the research fields a user is a part of.

        Args:
            user_id (int): user id of the first user to check against

        Returns:
            List[UserResearchFields]: List of research fields the user is apart of
        """
        stmt = select(UserResearchField).where(UserResearchField.user_id == user_id)
        try:
            result = self.session.scalars(stmt).all()
            return result
        except SQLAlchemyError as e:
            return []

    def get_by_user_and_reasearch_id(
        self, user_id: int, research_id: int
    ) -> Optional[UserResearchField]:
        """Checks if the user is in the given research id

        Args:
            user_id (int): User's id
            research_id (int): Research field id

        Returns:
            Optional[UserResearchField]: Returns the object if it exists otherwise None
        """
        stmt = select(UserResearchField).where(
            and_(
                UserResearchField.research_id == research_id,
                UserResearchField.user_id == user_id,
            )
        )
        try:
            result = self.session.scalars(stmt).first()
            return result
        except SQLAlchemyError as e:
            return None

    def remove(self, user_id: int, research_id: int) -> bool:
        """Remove a user from a research id

        Args:
            user_id (int): user id to remove
            research_id (int): research field id to remove from

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        stmt = delete(UserResearchField).where(
            and_(
                UserResearchField.user_id == user_id,
                UserResearchField.research_id == research_id,
            )
        )
        try:
            self.session.execute(stmt)
            return self.commit_changes()
        except SQLAlchemyError as e:
            self.session.rollback()
            return False
