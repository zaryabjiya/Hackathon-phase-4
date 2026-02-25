from fastapi import HTTPException, status, Depends, Header
from typing import Dict, Optional
from jose import jwt, JWTError
import os
import logging
from dotenv import load_dotenv
from pydantic import BaseModel

# Setup logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get the auth secret from environment - use SECRET_KEY to match auth.py
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Log configuration for debugging (don't log the actual secret)
logger.info(f"Middleware loaded: SECRET_KEY is {'set' if SECRET_KEY else 'MISSING'}, ALGORITHM={ALGORITHM}")


class TokenData(BaseModel):
    user_id: int
    email: Optional[str] = None
    username: Optional[str] = None


def verify_jwt_token(token: str) -> TokenData:
    """
    Verify JWT token and return user information
    Uses the same jose library and SECRET_KEY as routes/auth.py
    """
    try:
        logger.debug(f"Verifying JWT token: {token[:20]}...")
        # Decode the JWT token using the shared secret (same as auth.py)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"JWT payload: {payload}")

        # Extract user information from the token
        # auth.py creates tokens with: {"sub": user.email, "user_id": user.id, "username": user.username}
        user_id: int = payload.get("user_id")
        email: str = payload.get("sub")
        username: str = payload.get("username")

        if user_id is None:
            logger.warning("JWT token missing user_id")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

        token_data = TokenData(user_id=user_id, email=email, username=username)
        logger.info(f"Token validated for user_id={user_id}, email={email}")
        return token_data

    except JWTError as e:
        logger.error(f"JWT decode error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


def get_current_user(authorization: str = Header(...)) -> TokenData:
    """
    Dependency to get current user from JWT token in Authorization header
    Expected format: "Bearer <token>"
    """
    if not authorization or not authorization.startswith("Bearer "):
        logger.warning(f"Authorization header missing or malformed: {authorization}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing or malformed"
        )

    # Extract the token from the Authorization header
    token = authorization.split(" ")[1]
    logger.debug(f"Extracted token: {token[:20]}...")

    # Verify the token and get user information
    token_data = verify_jwt_token(token)

    return token_data