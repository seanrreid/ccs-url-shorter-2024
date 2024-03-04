from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker


from config import settings

DATABSE_URL = settings.DATABASE_URL

engine = create_engine(DATABSE_URL)
Session = sessionmaker(bind=engine)
session = Session()
