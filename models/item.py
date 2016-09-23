from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from utils.equip_slot import EquipSlots

from database import Base

__author__ = 'Hamster'


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)

    # Parent-CHILD one-to-many relationship to character
    char_id = Column(Integer, ForeignKey('character.id'))

    equipped = False
    slot = EquipSlots.NONE

    # PARENT-Child one-to-one relationship to ibase (item base), modifier and multiplier
    ibase = relationship('Item', uselist=False, back_populates='ibase')
    modifier = relationship('Item', uselist=False, back_populates='modifier')
    multiplier = relationship('Item', uselist=False, back_populates='multiplier')

    # todo init

    def print_item(self):
        str = 'This is {}.\n'.format(self.ibase.desc)
        if (self.slot != EquipSlots.NONE):
            str += 'Its {} {} {}.'.format(self.multiplier.desc, self.modifier.desc)
        return str
