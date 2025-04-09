"""Utility Module for extracting numbers"""

# Python Standard Library Imports
import re
import traceback

__all__ = ["parse_float", "parse_int"]


def parse_float(input_: str):
    """Parses a float(s) from a string, string can have characters

    Args:
        input (str): String with floats embedded

    Raises:
        TypeError: If the input is not a string
    Returns:
        list: returns list of all floats parsed, if only one returns as a singular
        not a list
    """
    try:
        # Verifying arguments
        if not isinstance(input_, str):
            raise TypeError("input image needs to be an ndarray")

        # Using regex expression to parse the numbers
        re_float = re.findall(r"[-+]?(?:\d*\.*\d+)", input_)

        # Checking if only 1 number was found
        if len(re_float) == 1:
            return float(re_float[0])

        # Converting all numbers found to floats
        re_float = [float(number) for number in re_float]

        return re_float
    except (TypeError, RuntimeError, ValueError) as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return None


def parse_int(input_: str):
    """Parses a float(s) from a string, string can have characters

    Args:
        input (str): String with floats embedded

    Raises:
        TypeError: If the input is not a string
    Returns:
        list: returns list of all floats parsed, if only one returns as a singular
        not a list
    """
    try:
        # Verifying arguments
        if not isinstance(input_, str):
            raise TypeError("input image needs to be an ndarray")

        # Using regex expression to parse the numbers
        re_float = re.findall(r"[-+]?(?:\d*\.*\d+)", input_)

        # Checking if only 1 number was found
        if len(re_float) == 1:
            return int(re_float[0])

        # Converting all numbers found to floats
        re_float = [int(number) for number in re_float]

        return re_float
    except (TypeError, RuntimeError, ValueError) as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return None
