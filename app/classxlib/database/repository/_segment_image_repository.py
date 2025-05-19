"""Database module for defining the SegmentImageRepository Class"""

# Python Third Party Imports
from sqlalchemy.orm import Session

# Local Library Imports
from ..model import SegmentImage
from ._base_repository import BaseRepository

__all__ = ['SegmentImageRepository']

class SegmentImageRepository(BaseRepository):
    """The class for interacting/querying the `segment_images` sql table.
        Args:
            session(sqlalchemy.orm.Session): The database session object
            to use for querying and commiting changes.
    """
    def __init__(self, session:Session):
        # Initializes the base repository class
        super().__init__(session=session,
                         model=SegmentImage,
                         table_name="segment_images")
