import jwt
from .schemas import TokenData

# Configuration for token validation
SECRET_KEY = "your-secret-key"  # Replace with your actual secret key
ALGORITHM = "HS256"


def verify_token(token: str) -> TokenData:
    """
    Verify and decode a JWT token.

    Args:
        token (str): The JWT token to decode.

    Returns:
        TokenData: Decoded data containing user information.

    Raises:
        ValueError: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise ValueError("Invalid token: user_id missing")
        return TokenData(user_id=user_id)
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
