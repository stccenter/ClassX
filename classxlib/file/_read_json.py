# Python Standard Library Imports
import os
import json
import traceback

__all__ = ["read_json"]

def read_json(directory: str, encoding: str = "utf-8") -> dict:
    """Reads Json files and returns them as dictionaries

    Args:
        directory (str): Directory path to json file
        encoding (str, optional): Encoding used when reading
        json file. Defaults to "utf-8".

    Raises:
        TypeError: If directory is not a string
        TypeError: If encoding is not a string

    Returns:
        dict: Dictionary of json file structure
    """
    try:
        # Verifying the arguments
        if not isinstance(directory, str):
            raise TypeError("TypeError: directory argument must be of type string")

        if not isinstance(encoding, str):
            raise TypeError("TypeError: encoding key needs to be of type string")

        # Verifying the file existance
        if os.path.isfile(directory):
            # Opening the json file as read only
            with open(directory, "r", encoding="utf-8") as json_file:
                # Loading the json data
                directory = json.load(json_file)

                # Closing the Json File
                json_file.close()
            return directory
        else:
            print("Error: File not found in directory:",directory)
            return None
    except (TypeError, OSError,
            FileNotFoundError) as error:
        print(error)
        traceback.print_tb(error.__traceback__)
        return None