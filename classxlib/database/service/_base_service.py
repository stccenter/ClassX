"""The BaseService class to act as a template for other services"""

# Third Party Imports
from sqlalchemy.orm import Session

# Local Library Imports
from ..repository import BaseRepository
from ..model import BaseModel


__all__ = ["BaseService"]


class BaseService:
    """The Base Service class for interacting with
    the repository classes.
    """

    def __init__(self, session: Session, repo: BaseRepository):
        self.session: Session = session
        self.repo: BaseRepository = repo(self.session)

    def add(self, database_obj: BaseModel):
        return self.repo.add_row(database_obj=database_obj)
