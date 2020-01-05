from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from sqlalchemy import Column, DateTime, Integer, String

# Defines connection engine to DB
engine = create_engine(
    'mysql+pymysql://sqlalchemy:password@localhost:5050/users')

# Connects to DB
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

# Creates the base reference for all SQLAlchemy classes
Base = declarative_base()
Base.query = db_session.query_property()
