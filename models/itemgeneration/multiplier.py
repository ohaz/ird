from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from utils.equip_slot import EquipSlots

from database import Base

__author__ = 'Hamster'


class Multiplier(Base):
    __tablename__ = 'multiplier'
    id = Column(Integer, primary_key=True)

    # CHILD-Parent one-to-one relationship to item
    item = relationship('Item', back_populates='modifier')

    # todo fill descriptions
    desc = Column(String(32))
    value = Column(Integer)

    # todo init
