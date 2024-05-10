import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from config import DATABASE_FILENAME

dirname = os.path.dirname(__file__)

db_url = os.path.join(dirname, "..", "data", DATABASE_FILENAME)

engine = create_engine(f'sqlite:///{db_url}')

session = sessionmaker(bind=engine)


def initialize_database():
    Base.metadata.create_all(engine)


def get_database_connection():
    return session
