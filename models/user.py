from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.room import Room
from models.character import Character
import hashlib
import time

__author__ = 'ohaz'


class User(Base):
    __tablename__ = 'user'

    # CHILD-Parent relationship to character
    user_name = Column(String(30), primary_key=True)
    character = relationship("Character", back_populates="user")
    character_id = Column(Integer, ForeignKey('character.id'))

    auth_key = Column(String(256))

    creation_date = Column(Integer)

    def print_stats(self):
        return self.character.print_stats()


def hash_key(key):
    return hashlib.sha256(key.encode('utf-8')).hexdigest()


def new_user(username, auth_key):
    return User(user_name=username, auth_key=hash_key(auth_key),
                creation_date=int(time.time()), character=Character(level=1))
