"""Security module for decoding tokens"""
# Python Standard Library Imports
import traceback

# Python Third Party Imports
import jwt

__all__ = ['decode_token']

def decode_token(token_str:str,secret:str) -> dict:
    """Decodes a token string back into a dictionary

    Args:
        token_str (str): Encoded token string
        secret (str): The encryption key to decode the token string.

    Raises:
        TypeError: If the Token is not a string.
        TypeError: If the Secret Key is not a string.

    Returns:
        dict: Returns a decoded dict from the encoded token string
    """
    try:
        # Verifying the arguments
        if not isinstance(token_str, str):
            raise TypeError("Token must be of type String")
        if not isinstance(secret, str):
            raise TypeError("Secret Key must be of type String")

        # Decoding token string
        decoded_token = jwt.decode(token_str, secret, algorithms=["HS256"])
        return decoded_token
    except (RuntimeError, TypeError) as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return None
