from config import SQLALCHEMY_DATABASE_URI

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

DB_session = sessionmaker(bind=engine)

