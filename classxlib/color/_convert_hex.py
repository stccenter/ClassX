"""Submodule for converting colors to different formats"""

# Python Standard Library Imports
import traceback


def hex2rgb(hex_code: str) -> tuple:
    """Converts a hex color code into a RGB tuple

    Args:
        hex_code (str): The hex code to be converted input can have a # or not.

    Raises:
        TypeError: If input hex code is not of type String

    Returns:
        tuple: Returns an 8 bit RGB tuple in this format (R,G,B).
    """
    try:
        # Verifying the arguments
        if not isinstance(hex_code, str):
            raise TypeError("Hex code needs to be of type String")

        # Extracts the RGB values from the hexadecimal code.
        return tuple(int(hex_code.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
    except (TypeError, ValueError, RuntimeError) as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return None
