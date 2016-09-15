from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

__author__ = 'ohaz'

engine = create_engine('sqlite:///ird.sqlite', echo=False)

Base = declarative_base()

Session_maker = sessionmaker(bind=engine)
session = Session_maker()
