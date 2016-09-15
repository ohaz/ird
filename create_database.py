from sqlalchemy_utils import database_exists, create_database
from database import engine, Base
from models.user import User
from models.room import Room

__author__ = 'ohaz'


if __name__ == '__main__':

    if not database_exists(engine.url):
        print('Creating DB')
        create_database(engine.url)
        Base.metadata.create_all(engine)
