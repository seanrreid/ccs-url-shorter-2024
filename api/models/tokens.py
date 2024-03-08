from sqlalchemy import Column, String, Integer, DateTime, func
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from config import settings
from db import session
from models.base import Base

import jwt


class BlacklistedToken(Base):
    __tablename__ = 'blacklisted_tokens'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    token = Column(String)

    def __repr__(self):
        return f"<BlacklistedToken(id={self.id}, created_at={self.created_at})>"


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: str | None = None


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    # Make a copy so we don't mutate the original data
    to_encode = data.copy()

    if expires_delta:
        # If an expires_delta is provided, the expiration time (expire) is set to the current UTC time plus the  delta.
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # If expires_delta is not provided, the default expiration time is set to 15 minutes from the current UTC time.
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    # Add the expiration to the JWT
    to_encode.update({"exp": expire})
    # Actually encode our JWT with the data/time settings
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


def is_token_blacklisted(token):
    # Check if the token is blacklisted in the database
    return session.query(BlacklistedToken).filter_by(token=token, is_blacklisted=True).first() is not None
