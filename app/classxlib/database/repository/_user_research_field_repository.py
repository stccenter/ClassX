"""Database module for defining the UserResearchFieldRepository Class"""

# Python Third Party Imports
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

# Local Library Imports
from ..model import UserResearchField
from ._base_repository import BaseRepository

__all__ = ['UserResearchFieldRepository']
class UserResearchFieldRepository(BaseRepository):
    """The class for interacting/querying the `user_friends` sql table.
        Args:
            session(sqlalchemy.orm.Session): The database session object
            to use for querying and commiting changes.
    """

    def __init__(self, session:Session):
        # Initializes the base repository class
        super().__init__(session=session,
                         model=UserResearchField,
                         table_name="user_research_fields")

    def get_research_ids(self, user_id: int):
        """Gets all the research fields a user is a part of.

        Args:
            user_id (int): user id of the first user to check against

        Returns:
            List[UserResearchFields]: List of research fields the user is apart of

        """

        # Filtering by the user id
        return self.session.query(UserResearchField).\
            filter(UserResearchField.user_id == user_id).all()
    
    def get_by_user_and_reasearch_id(self, user_id, research_id):
        """Checks if the user is in the given reearch id

        Args:
            user_id (int): User's id
            research_id (int): User

        Returns:
            user_research_field_obj: Returns the object if it exists otherwise None
        """
        return self.session.query(UserResearchField).\
        filter(and_(UserResearchField.research_id == research_id, UserResearchField.user_id == user_id))
    
    def remove(self, user_id, research_id):
        """Remove a user from a research id

        Args:
            user_id (int): user id to remove
            research_id (int): research field id to remove from

        Returns:
            user_research_field_obj: user research field object if deleted
        """
        return self.session.delete(UserResearchField).\
        filter(and_(UserResearchField.user_id == user_id, UserResearchField.research_id == research_id)).all()
