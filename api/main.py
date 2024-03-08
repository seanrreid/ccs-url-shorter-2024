import jwt
from fastapi import FastAPI, HTTPException, status, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from starlette.responses import RedirectResponse
from datetime import date, timedelta

# Import our tools
# This is the database connection file
from db import engine, session
from config import settings

# These are our models
from models.base import Base
from models.links import Links, LinksSchema
from models.users import User, UserBaseSchema, UserSchema, UserAccountSchema
from models.tokens import Token, BlacklistedToken, generate_token
from services import get_current_user_token, create_user, get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


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


@app.get("/sendit")
async def redirect_to_external_url(url: str = Query(...)):
    # The ellipsis (...) is a special value in FastAPI that
    # indicates the parameter is required.
    # It means that the "url" parameter must be present
    # in the request, and its value must not be None.

    # Find the long url via the short
    link = session.query(Links).filter(Links.short_url == url).first()

    # Add the https protocol
    long_url = f"https://{link.long_url}"

    # redirect
    return RedirectResponse(long_url)


@app.post('/register', response_model=UserSchema)
def register_user(payload: UserAccountSchema):
    """Processes request to register user account."""
    payload.hashed_password = User.hash_password(payload.hashed_password)
    return create_user(user=payload)


@app.post('/login', status_code=200)
async def login(payload: UserAccountSchema):
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

    """
    Refresh Token Flow
    https://www.digitalocean.com/community/tutorials/an-introduction-to-oauth-2#refresh-token-flow
    """

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = generate_token(
        data={"email": user.email}, expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(
        minutes=settings.REFRESH_TOKEN_EXPIRES_MINUTES)
    refresh_token = generate_token(
        data={"email": user.email}, expires_delta=refresh_token_expires
    )
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@app.get('/logout', status_code=200)
def logout(token: Token = Depends(oauth2_scheme)):
    try:
        token = BlacklistedToken(token=token)
        session.add(token)
        session.commit()
    except IntegrityError as e:
        raise settings.CREDENTIALS_EXCEPTION
    return {"details:": "Logged out"}


@app.get('/getUser', status_code=200)
async def get_user_id(current_user: str = Depends(get_current_user_token)):
    return {"email": current_user.email, "id": current_user.id}


@app.post('/links/add', status_code=200)
async def add_link(link_data: LinksSchema):
    link = Links(**link_data.dict())
    session.add(link)
    session.commit()
    return {"Link added:": link.title}
