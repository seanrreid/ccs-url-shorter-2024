from sqlalchemy import Column, Integer, String, UniqueConstraint, LargeBinary
from pydantic import BaseModel, Field

import bcrypt
import jwt

from config import settings
from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(225), unique=True)
    hashed_password = Column(LargeBinary)

    UniqueConstraint("email", name="uq_user_email")

    def __repr__(self):
        """Returns string representation of model instance"""
        """ !r means the value is formatted using its
            __repr__ method rather than its __str__ method."""
        return f"<User {self.email!r}>"

    @staticmethod
    def hash_password(password) -> str:
        """Transforms password from it's raw textual form to
        cryptographic hashes
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def validate_password(self, pwd) -> bool:
        return bcrypt.checkpw(password=pwd.encode(), hashed_password=self.hashed_password)

    def generate_token(self) -> dict:
        """Generate our JWT"""
        return {
            "access_token": jwt.encode(
                {"email": self.email},
                settings.SECRET_KEY
            )
        }


class UserBaseSchema(BaseModel):
    email: str


class UserSchema(UserBaseSchema):
    id: int

    class Config:
        populate_by_name = True


class UserAccountSchema(UserBaseSchema):
    """ We set an alias for the field so that when this field is serialized or deserialized,
    the name "password" will be used instead of "hashed_password." """
    hashed_password: str = Field(alias="password")
