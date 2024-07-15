from typing import Optional
import redis.asyncio as redis

from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.database.db import get_db
from dotenv import load_dotenv
from src.database.models import User
import os

load_dotenv()


class Auth:
    """
    Handles authentication operations such as password hashing, token creation, and verification.
    """

    pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ALGORITHM: str = os.getenv("ALGORITHM")
    oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
    r: redis.Redis = redis.Redis(
        host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), db=0
    )

    def verify_password(self, plain_pass: str, hash_pass: str) -> bool:
        """
        Verifies if the plain password matches the hashed password.
        :param plain_pass: Plain password to verify.
        :param hash_pass: Hashed password to compare against.
        :return: True if the passwords match, False otherwise.
        """

        return self.pwd_context.verify(plain_pass, hash_pass)

    def get_password_hash(self, password: str) -> str:
        """
        Hashes the provided password.
        :param password: Password to hash.
        :return: Hashed password.
        """
        return self.pwd_context.hash(password)

    async def create_access_token(
        self, data: dict, expires_delta: Optional[float] = None
    ) -> str:
        """
        Creates an access token based on the provided data.
        :param data: Data to encode into the token.
        :param expires_delta: Expiration time delta in seconds (optional).
        :return: Encoded access token.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
        encoded_access_token: str = jwt.encode(to_encode, self.SECRET_KEY, self.ALGORITHM)
        return encoded_access_token

    async def create_refresh_token(
            self, data: dict, expires_delta: Optional[float] = None
    ) -> str:
        """
        Creates a refresh token based on the provided data.
        :param data: Data to encode into the token.
        :param expires_delta: Expiration time delta in seconds (optional).
        :return: Encoded refresh token.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token: str = jwt.encode(to_encode, self.SECRET_KEY, self.ALGORITHM)
        return encoded_refresh_token

    async def decode_refresh_token(self, token: str) -> str:
        """
        Decodes the refresh token to retrieve the email associated with it.
        :param token: Refresh token to decode.
        :return: Decoded email from the token.
        :raises HTTPException 401: If the token is invalid or has an incorrect scope.
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload.get("sub")
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            ) from e

    @staticmethod
    async def authenticate_user(email: str, password: str, db: Session = Depends(get_db)) -> Optional[User]:
        """
        Authenticates a user based on email and password.
        """
        from src.services.user_service import authenticate_user
        user = authenticate_user(email, password, db)
        return user

    async def get_email_from_token(self, token: str) -> str:
        """
        Retrieves the email from the provided email verification token.
        :param token: Email verification token to decode.
        :return: Decoded email from the token.
        :raises HTTPException 422: If the token is invalid.
        """

        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload.get("sub")
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            ) from e


auth_service = Auth()
