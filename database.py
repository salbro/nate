import json
from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from tfy_db_credentials import tfy_db_url

################### SQL ##########################
engine = create_engine(tfy_db_url, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
db_session.close()

### this location is crucial. after BASE declared but before def init_db()
from models import *


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.create_all(engine)

# init_db() no need to run if tables already in SQL DB
