import json
from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

################### SQL ##########################
with open("db_credentials.json", "r") as fp:
    db_info = json.load(fp)

url = "mysql+pymysql://"+db_info['username']+":"+db_info['password']+"@"+db_info['endpoint']+"/"+db_info['name']
engine = create_engine(url, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

################## SQL #########################
Base = declarative_base()
Base.query = db_session.query_property()

### this location is crucial. after BASE has been declared
# but before init_db() is defined
from users import *


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    ### DONT CALL THIS IF ALREADY CREATED?
    Base.metadata.create_all(engine)

# init_db()
