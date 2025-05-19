"""Database module for UserResearchFieldService class that interacts
with the `user_research_fields` table"""

# Third Party Imports
from sqlalchemy.orm import Session

# Local Library Imports
from ..repository import UserResearchFieldRepository
from ._base_service import BaseService
from ..model import UserResearchField

__all__ = ['UserResearchFieldService']

class UserResearchFieldService(BaseService):
    """The User Research Field Service class for interacting with
    the repository classes.
    """

    def __init__(self, session:Session):
        # Initializing the repository and distributing the
        # database session
        super().__init__(session, UserResearchFieldRepository)
        self.repo : UserResearchFieldRepository

    

    def get_user_research_fields(self, user_id: int):
        """Service function for getting research fields a user is a part of
        Args:
            user_int (int): user id to see their research fields
        Returns:
            list(user_research_field)s: List of user_to_research_field rows
        """
        return self.repo.get_research_ids(user_id)
    

    def add_research_field(self, user_id: int, research_field: int, role_id: int = 0):
        """Service function for adding a user level to the
        database
        Args:
            user_id (int): user id to get requests for 
        Returns:
            user_friend_objs List(UserFriend): Requests that are pending 
        """
        row = UserResearchField(user_id, research_field, role_id)
        return self.repo.add_row(row)
    
    def remove_research_field(self, user_id: int, research_field_id: int):
        """Service function denying a friend request
        Args:
            user_id (int): user Id who is denying the request
            research_field_id (int): research field id to remove from
        Returns:
            user_friend_obj: The newly added UserLevel. Will be None if it
            fails.
        """
        return self.repo.remove(user_id, research_field_id)
    
    def in_research_id(self, user_id: int, research_field_id: int):
        """Service function checking if a user is in a research field
        Args:
            user_id (int): user who is sending the block
            research_field_id (int): research field to check against
        Returns:
            True if they're in the research field otherwise False
        """
        
        row = self.repo.get_by_user_and_reasearch_id(user_id, research_field_id)
        return True if row else False
    
