from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

__author__='Hamster'


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key = True)

    # Parent-CHILD one-to-many relationship to character
    char_id = Column(Integer, ForeignKey('character.id'))

    equipped = False