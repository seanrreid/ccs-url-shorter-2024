from sqlalchemy import Column, String, Integer, DateTime, func
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from config import settings

from models.base import Base

import jwt


class Token(Base):
    __tablename__: 'blacklist'
    id = Column(Integer, primary_key=True)
    token = Column(String)

class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: str | None = None


class BlacklistedToken(Base):
    __tablename__ = 'blacklisted_tokens'

    id = Column(String, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<BlacklistedToken(id={self.id}, created_at={self.created_at})>"

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

    if is_token_blacklisted(encoded_jwt):
        raise ValueError("Token is blacklisted")

    return encoded_jwt


def is_token_blacklisted(token):
    # Check if the token is blacklisted in the database
    return BlacklistedToken.objects.filter(token=token).exists()
