from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from utils.equip_slot import EquipSlots

from database import Base

__author__ = 'Hamster'


class Modifier(Base):
    __tablename__ = 'modifier'
    id = Column(String)

    # CHILD-Parent one-to-one relationship to item
    item = relationship('Item', back_populates='modifier')

    material = Column(Integer)
    desc = Column(String(32))

    # todo init
