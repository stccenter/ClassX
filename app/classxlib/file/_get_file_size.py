"""Gets the file data size from a given directory
    in a specified type"""
# Python Standard Library Imports
import os
import traceback

__all__ = ['get_file_size']

def get_file_size(dir_:str, type_:str="mb") -> float:
    """Gets the file data size from a given directory
    in a specified type

    Args:
        dir_ (str): The directory of the file to check
        type_ (str): Keyword for which type the size should be
                    returned as, e.g. mb(megabytes), kb(kilobytes),
                    b(bytes) Default Value is `mb`
    Raises:
        ValueError: If the directory is not a string
        TypeError: If the type is not a string
        KeyError: If the type is not an accepted key
                  (b, kb, mb, gb, tb, pb)

    Returns:
        float: Number of bytes as a float
    """
    # Verifying arguments
    if not isinstance(dir_, str):
        raise TypeError("TypeError: directory argument must be of type string")
    if type_ not in ['b', 'kb', 'mb', 'gb',
                    'tb', 'pb']:
        raise KeyError("Unknown datatype key used")
    try:
        # Getting size of file
        if type_.lower() == 'b': # Bytes
            size = os.path.getsize(dir_)
        if type_.lower() == 'kb': # Kilobytes
            size = os.path.getsize(dir_) / 1024
        if type_.lower() == 'mb': # Megabytes
            size = os.path.getsize(dir_) /(1024*1024)
        if type_.lower() == 'gb': # Gigabytes
            size = os.path.getsize(dir_) /(1024*1024*1024)
        if type_.lower() == 'tb': # Terabytes
            size = os.path.getsize(dir_) /(1024*1024*1024*1024)
        if type_.lower() == 'pb': # Petabytes
            size = os.path.getsize(dir_) /(1024*1024*1024*1024)

        return size
    except (OSError, ValueError,
            RuntimeError, TypeError,
            KeyError) as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return 0
