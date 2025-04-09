"""Security module for encoding tokens"""

# Python Standard Library Imports
import traceback

# Python Third Party Imports
import jwt

__all__ = ["encode_token"]


def encode_token(payload: dict, secret: str) -> str:
    """Encodes a token string using an encryption key.

    Args:
        payload (dict): The payload to encode
        secret (str): The encryption key to encode the payload.

    Raises:
        TypeError: If the payload is not a dictionary
        TypeError: If the Secret Key is not a string.

    Returns:
        str: Returns encoded token string
    """
    try:
        # Verifying the arguments
        if not isinstance(payload, dict):
            raise TypeError("Payload must be a dictionary")
        if not isinstance(secret, str):
            raise TypeError("Secret Key must be of type String")

        # Encoding token string
        encoded_token = jwt.encode(payload, secret, algorithm="HS256")
        return encoded_token
    except (RuntimeError, TypeError) as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return None
