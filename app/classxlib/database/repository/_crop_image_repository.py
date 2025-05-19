"""Database module for defining the CropImageRepository Class"""

# Python Third Party Imports
from sqlalchemy.orm import Session

# Local Library Imports
from ..model import CropImage
from ._base_repository import BaseRepository

__all__ = ['CropImageRepository']

class CropImageRepository(BaseRepository):
    """The class for interacting/querying the `crop_images` sql table.
        Args:
            session(sqlalchemy.orm.Session): The database session object
            to use for querying and commiting changes.
    """
    def __init__(self, session:Session):
        # Initializes the base repository class
        super().__init__(session=session,
                         model=CropImage,
                         table_name="crop_images")
