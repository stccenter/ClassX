"""Converts a given filepath into a format
that is compatible for storage in the database."""
# Python Standard Library Imports
import traceback

__all__ = ['format_database_path']

def format_database_path(dir_:str)->str:
    """Converts a given filepath into a format
    that is compatible for storage in the database.

    Args:
        dir_ (str): Directory path to be converted

    Raises:
        ValueError: If the directory argument is not of type String

    Returns:
        str: Formatted directory for saving in database
    """
    # Verifying the arguments
    if not isinstance(dir_, str):
        raise ValueError("ValueError: directory argument must be of type string")
    try:
        # This removes the first two folders from the directory
        return '/'.join(dir_.replace('\\', '/').strip('/').split('/')[1:])

    except (RuntimeError) as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return None
