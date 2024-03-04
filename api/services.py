from models.users import User, UserAccountSchema
from db import session


def create_user(user: UserAccountSchema):
    db_user = User(**user.dict())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user(email: str):
    return session.query(User).filter(User.email == email).one()