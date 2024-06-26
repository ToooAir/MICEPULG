from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

db_session = scoped_session(sessionmaker(bind=engine, autoflush=True))
