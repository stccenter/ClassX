"""Database module for defining the OriginalImageRepository Class"""

# Python Third Party Imports
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from sqlalchemy.sql import and_, or_

# Local Library Imports
from ..model import OriginalImage
from ._base_repository import BaseRepository

__all__ = ["OriginalImageRepository"]


class OriginalImageRepository(BaseRepository):
    """The class for interacting/querying the `original_images` sql table.
    Args:
        session(sqlalchemy.orm.Session): The database session object
        to use for querying and committing changes.
    """

    def __init__(self, session: Session):
        # Initializes the base repository class
        super().__init__(
            session=session, model=OriginalImage, table_name="original_images"
        )

    def get_by_query_user_id_research_id(
        self, query: str, user_id: int, research_id: int, default_id: int = None
    ):
        """Gets an original image by a search query, user ID, research ID,
        and optionally the default user id if provided. The search query sees if a
        name matches the file name or the alias.

        Args:
            query (str): The search query for matching names. Only needs to match part of the name.
            user_id (int): The ID of the user associated with the image.
            research_id (int): The ID of the research field associated with the image.
            default_id (int): The ID of the default user to also filter by.
            Defaults to None.

        Returns:
            List[OriginalImage]: A list of OriginalImage objects with the filters applied.
        """

        # Create a list of user IDs to filter on, including the default_id if provided
        user_ids = [user_id]
        if default_id is not None:
            user_ids.append(default_id)

        stmt = select(OriginalImage).where(
            and_(
                OriginalImage.user_id.in_(user_ids),
                or_(
                    OriginalImage.name.contains(query),
                    OriginalImage.alias.contains(query),
                ),
                OriginalImage.research_id == research_id,
            )
        )

        try:
            results = self.session.scalars().all()
            return results
        except Exception as e:
            print(
                f"Error fetching original images with query '{query}', user_id {user_id}, and research_id {research_id}"
            )
            print(e)
            return []

    def update_alias_by_id(
        self, original_image_id: int, new_alias: str
    ) -> Optional[OriginalImage]:
        """Updates the alias of a given original image

        Args:
            original_image_id (int): The ID of the original image to update
            new_alias (str): The new alias name.

        Returns:
            Optional[OriginalImage]: The original image database object with the updated
            alias. Returns None if there is an error.
        """
        stmt = (
            update(OriginalImage)
            .where(OriginalImage.id == original_image_id)
            .values(alias=new_alias)
            .returning(OriginalImage)
        )

        try:
            result = self.session.scalars(stmt).first()
            self.commit_changes()
            return result
        except Exception as e:
            print(f"Error updating alias for original_image_id {original_image_id}")
            print(e)
            return None
