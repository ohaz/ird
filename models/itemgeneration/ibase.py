from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from utils.equip_slot import EquipSlots

from database import Base

__author__ = 'Hamster'


class IBase(Base):
    __tablename__ = 'ibase'
    id = Column(String(32), primary_key=True)

    # CHILD-Parent one-to-one relationship to item
    item = relationship('Item', back_populates='ibase')

    lowdmg = Column(Integer)
    highdmg = Column(Integer)
    scaling = Column(String(10))
    armor = Column(Integer)
    equip = Column(Integer)
    desc = Column(String(64))

    # todo init
