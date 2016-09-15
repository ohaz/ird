from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.room import Room
import hashlib
import time

__author__ = 'ohaz'


class User(Base):
    __tablename__ = 'user'
    character_name = Column(String(30), primary_key=True)
    auth_key = Column(String(256))
    hp = Column(Integer)
    max_hp = Column(Integer)
    strength = Column(Integer)
    dexterity = Column(Integer)
    constitution = Column(Integer)
    intelligence = Column(Integer)
    wisdom = Column(Integer)
    charisma = Column(Integer)
    creation_date = Column(Integer)

    location_id = Column(Integer, ForeignKey('room.id'))
    location = relationship('Room', back_populates='users')

    def print_stats(self):
        return 'STR: {} DEX: {} CON: {} INT: {} WIS: {} CHA: {}'.format(self.strength, self.dexterity,
                                                                        self.constitution, self.intelligence,
                                                                        self.wisdom, self.charisma)


def hash_key(key):
    return hashlib.sha256(key.encode('utf-8')).hexdigest()


def new_user(username, auth_key, stats):
    return User(character_name=username, auth_key=hash_key(auth_key), strength=stats[0], dexterity=stats[1],
                constitution=stats[2], intelligence=stats[3], wisdom=stats[4], charisma=stats[5], hp=0, max_hp=0,
                creation_date=int(time.time()))


def set_stats(user, stats):
    user.strength = stats[0]
    user.dexterity = stats[1]
    user.constitution = stats[2]
    user.intelligence = stats[3]
    user.wisdom = stats[4]
    user.charisma = stats[5]
