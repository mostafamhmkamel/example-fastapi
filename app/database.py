from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

#the purpose of this python file is to connect sqlalchemy to the database

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
#format: 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

engine = create_engine(SQLALCHEMY_DATABASE_URL) #responsible for sqlalchemy connecting to postgres

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind = engine) #to talk to database, session is needed

Base = declarative_base() #all of the models for our tables will be extending from this class

# function for creating a session with database, this will be our window of sending requests
# we will call on to it when we make a request, and it will close once the request is executed

def get_db():         
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
