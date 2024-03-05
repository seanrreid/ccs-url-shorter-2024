from typing import Dict
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import date

# Import our tools
# This is the database connection file
from db import engine, session
from config import settings

# These are our models
from models.base import Base
from models.links import Links, LinksSchema
from models.users import User, UserSchema, UserAccountSchema
from services import create_user, get_user


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,
                  version=settings.PROJECT_VERSION)
    create_tables()
    return app


app = start_application()

# Setup our origins...
# ...for now it's just our local environments
origins = [
    "http://localhost:5173"
]

# Add the CORS middleware...
# ...this will pass the proper CORS headers
# https://fastapi.tiangolo.com/tutorial/middleware/
# https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Root Route"}


@app.get('/links')
def get_links():
    links = session.query(Links)
    return links.all()


@app.post('/links/add')
async def add_link(link_data: LinksSchema):
    link = Links(**link_data.dict())
    session.add(link)
    session.commit()
    return {"Link Added": link.title}


@app.post('/register', response_model=UserSchema)
def register_user(payload: UserAccountSchema):
    """Processes request to register user account."""
    payload.hashed_password = User.hash_password(payload.hashed_password)
    return create_user(user=payload)


@app.post('/login', response_model=Dict)
async def login(payload: UserAccountSchema, status_code=200):
    try:
        user: User = get_user(email=payload.email)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials"
        )

    is_validated: bool = user.validate_password(payload.hashed_password)

    if not is_validated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials"
        )

    return user.generate_token()

@app.post('/verify')
async def verify_token(payload):
    is_verified: bool = user.verify_token(payload.token)