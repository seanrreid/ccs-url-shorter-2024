from fastapi import HTTPException, status, Query, Depends
from fastapi.security import OAuth2PasswordBearer
from models.users import User, UserAccountSchema
from models.tokens import TokenData
from db import session
from config import settings

import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# I'm on the fence about seperating these methods into this file
# There's a case to be made that they could also work in the model as static methods?

def create_user(user: UserAccountSchema):
    db_user = User(**user.dict())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user(email: str):
    return session.query(User).filter(User.email == email).one()


async def get_current_user_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    except jwt.DecodeError:
        raise credentials_exception
    user = session.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user
