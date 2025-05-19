"""Database module for defining the BaseRepository Class"""

# Python Standard Library Imports
import traceback
from typing import Any, Dict

# Python Third Party Imports
from sqlalchemy.exc import (SQLAlchemyError, DBAPIError,
                            DatabaseError)
from sqlalchemy.orm import Session, Query

__all__ = ['BaseRepository']

class BaseRepository:
    """The base class for interacting/querying the `table_name` sql table.
        Args:
            session(sqlalchemy.orm.Session): The database session object
            to use for querying and commiting changes.
            table_name(str): The name of the table in the SQL Database
            model: The python model class for the database
    """
    def __init__(self, session:Session, table_name:str, model):
        self.session : Session = session
        self.table_name: str = table_name
        self.model = model
        self.attributes = self.model.__annotations__.keys()

    def commit_changes(self):
        """Utility function to commit changes to the database
        """
        try:
            # Commiting the changes
            self.session.commit()
            return True
        except (SQLAlchemyError, DatabaseError,
                DBAPIError, RuntimeError) as error:
            print("Error commiting changes to " + self.table_name +" table")
            print(error)
            traceback.print_tb(error.__traceback__)
            # Rollsback incase of corruption errors
            self.session.rollback()
            return False

    def add_row(self, database_obj):
        """Adds a new row to the a database
        table

        Args:
            database_obj: The database object to add to the
            database

        Returns:
            DatabaseModel: Returns the database object added
            to it's respective table.
        """
        # Adding crop image to session instance
        self.session.add(database_obj)

        # Commiting the changes to the database
        if self.commit_changes() is False:
            return None

        return database_obj

    def get_by_id(self, object_id:int):
        """Gets an database object by their ID. This function
        requires the table to have `id` as a column.

        Args:
            object_id (int): The ID associated with a table row.

        Returns:
            DatabaseModel: The database row represented as a
            python dataclass
        """
        if 'id' not in self.attributes:
            raise SQLAlchemyError("Error: This table does not have an id column")
        # Filtering by the original image id
        database_obj = self.session.query(self.model).\
            filter(self.model.id == object_id).first()

        return database_obj

    def delete_row_by_id(self, object_id:int):
        """Deletes a row by their ID from the database. This function
        requires the table to have `id` as a column.

        Args:
            object_id (int): The ID associated with a table row.
        """
        if 'id' not in self.attributes:
            raise SQLAlchemyError("Error: This table does not have an id column")

        # Filtering by the crop image id then deleting
        self.session.query(self.model).\
            filter(self.model.id == object_id).delete()

        # Commiting the changes to the database
        if self.commit_changes() is False:
            return False

        return True

    def get_by_ids(self, object_id_list:list):
        """Gets a list of rows by a list of IDs from the database.
        This function requires the table to have `id` as a column.

        Args:
            object_id_list (list): The list of row ids
            to check.

        Returns:
            list(BaseModel): The list of database objects, Returns
            an empty list if none found.
        """
        if 'id' not in self.attributes:
            raise SQLAlchemyError("Error: This table does not have an id column")
        # Filtering by the crop image id list
        database_obj_list = self.session.query(self.model).\
            filter(self.model.id.in_(object_id_list)).all()

        return database_obj_list

    def get_first_by_args(self,**kwargs):
        """Gets a database by using keyword arguments provided. The keyword arguments must match
        the column names in the database table. This function requires `user_id` to be a column.

        Args:
            **kwargs (Any): A list of provided keyword arguments these must match
            the database column names.
        Returns:
            BaseModel: The database object, Returns None if not found.
        """

        database_obj = self.session.query(self.model).\
            filter_by(**kwargs).first()
        return database_obj

    def get_all_by_args(self,**kwargs):
        """Gets a list of database objects by keyword arguments provided. The keyword arguments
        must match the column names in the database table.

        Args:
            **kwargs (Any): A list of provided keyword arguments these must match
            the database column names.
        Returns:
            list(BaseModel): The list of database objects, Returns
            an empty list if none found.
        """

        database_obj_list = self.session.query(self.model).\
            filter_by(**kwargs).all()
        return database_obj_list

    def get_first_by_user_id_args(self,
                                  user_id:int,
                                  default_id:int = None,
                                  **kwargs):
        """Gets a database by using the user id, default id(if provided),
        and keyword arguments provided. The keyword arguments must match the column names in
        the database table. This function requires `user_id` to be a column.

        Args:
            user_id (int): The ID of the user associated with the image.
            default_id (int): The ID of the default user to also filter by.
            Defaults to None.
            **kwargs (Any): A list of provided keyword arguments these must match
            the database column names.
        Returns:
            BaseModel: The database object, Returns None if not found.
        """
        if 'user_id' not in self.attributes:
            raise SQLAlchemyError("Error: This table does not have an user_id column")

        database_obj = self.session.query(self.model).\
            filter(self.model.user_id.in_((user_id,default_id))).filter_by(**kwargs).first()
        return database_obj

    def get_all_by_user_id_args(self,
                                user_id:int,
                                default_id:int = None,
                                **kwargs):
        """Gets a list of database objects by using the user id, default id(if provided),
        and keyword arguments provided. The keyword arguments must match the column names in
        the database table. This function requires `user_id` to be a column.

        Args:
            user_id (int): The ID of the user associated with the image.
            default_id (int): The ID of the default user to also filter by.
            Defaults to None.
            **kwargs (Any): A list of provided keyword arguments these must match
            the database column names.
        Returns:
            list(BaseModel): The list of database objects, Returns
            an empty list if none found.
        """
        if 'user_id' not in self.attributes:
            raise SQLAlchemyError("Error: This table does not have an user_id column")

        database_obj_list = self.session.query(self.model).\
            filter(self.model.user_id.in_((user_id,default_id))).filter_by(**kwargs).all()
        return database_obj_list
    
    def query_by_dict(self, filters: Dict[str, Any], one: bool = True):
        """Query current database table using a dictionary

        Args:
            filters(dict): The dictionary of filters to apply to the query
            one(bool): If true, returns the first result, otherwise returns all
        Returns:
            list(BaseModel): The list of database objects, Returns
            an empty list if none found.
        """
        query: Query = Query(self.model, self.session)


        for col, value in filters.items():
            if col not in self.attributes:
                continue
            query = query.filter(self.attributes[col] == value)

        if one:
            results = query.limit(1).first()
        else:
           results = query.all()

        return results

