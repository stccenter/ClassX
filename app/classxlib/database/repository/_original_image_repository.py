"""Database module for defining the OriginalImageRepository Class"""

# Python Third Party Imports
from sqlalchemy.orm import Session, Query
from sqlalchemy.sql import and_, or_

# Local Library Imports
from ..model import OriginalImage
from ._base_repository import BaseRepository

__all__ = ['OriginalImageRepository']

class OriginalImageRepository(BaseRepository):
    """The class for interacting/querying the `original_images` sql table.
        Args:
            session(sqlalchemy.orm.Session): The database session object
            to use for querying and commiting changes.
    """
    def __init__(self, session:Session):
        # Initializes the base repository class
        super().__init__(session=session,
                         model=OriginalImage,
                         table_name="crop_images")

    def get_by_query_user_id_research_id(self,
                                         query:str,
                                         user_id:int,
                                         research_id:int,
                                         default_id:int=None) -> Query:
        """Gets a original image by a search query, user ID, research ID,
        and optionally the default user id if provided. The search query sees if a
        name matches the file name or the alias

        Args:
            query (str): The search query for matching names. Only needs to match part of the name.
            user_id (int): The ID of the user associated with the image.
            research_id (int): The ID of the research field associated with the image.
            default_id (int): The ID of the default user to also filter by.
            Defaults to None.

        Returns:
            Query: An SQLalchemy query object with the filters applied.
        """

        # Filtering by the original image id, user id, default id and a name search query
        original_image_obj_list = self.session.query(OriginalImage).\
            filter(and_(OriginalImage.user_id.in_((user_id, default_id)),
                        or_(OriginalImage.name.contains(query),OriginalImage.alias.contains(query)),
                        OriginalImage.research_id == research_id))

        return original_image_obj_list

    def update_alias_by_id(self,
                           original_image_id:int,
                           new_alias:str):
        """Updates the alias of a given original image

        Args:
            original_image_id (int): The ID of the original image to update
            new_alias (str): The new alias name.

        Returns:
            OriginalImage: The original image database object with the updated
            alias. Returns None if there is an error.
        """
        # Filtering by the original image id
        original_image_obj = self.session.query(OriginalImage).\
            filter(OriginalImage.id == original_image_id).first()

        # Overwriting the current alias
        original_image_obj.alias = new_alias

        # Commiting the changes to the database
        if self.commit_changes() is False:
            return None

        return original_image_obj
