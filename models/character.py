from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from utils import utils
from database import Base
from models.room import Room

__author__ = 'Hamster'


class Character(Base):
    __tablename__ = 'character'
    id = Column(Integer, primary_key=True)

    # PARENT-Child one-to-one relationship to user
    user = relationship("User", uselist=False, back_populates="character")

    # PARENT-Child one-to-many relationship to item
    inventory = relationship("Item")

    # Parent-CHILD one-to-many relationship to room
    room_id = Column(Integer, ForeignKey('room.id'))
    room = relationship("Room", back_populates="characters")

    # properties
    level = Column(Integer)
    hp = Column(Integer)
    max_hp = Column(Integer)
    strength = Column(Integer)
    dexterity = Column(Integer)
    constitution = Column(Integer)
    intelligence = Column(Integer)
    wisdom = Column(Integer)
    charisma = Column(Integer)

    equipable_items = Column(Integer)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.roll_stats()

    def roll_stats(self):
        stats = utils.generate_stats(self.level)
        self.strength = stats[0]
        self.dexterity = stats[1]
        self.constitution = stats[2]
        self.intelligence = stats[3]
        self.wisdom = stats[4]
        self.charisma = stats[5]

        self.max_hp = 20 + 3 * self.constitution
        self.hp = self.max_hp

    def move(self, targetRoom):
        if self.room_id == targetRoom.id:
            return "You are already in this room."
        elif (self.room is not None) and (targetRoom not in self.room.exits):
            return "There is no such exit."
        self.room = targetRoom
        self.room_id = targetRoom.id
        return self.room.get_description()


    def print_stats(self):
        return 'STR: {} DEX: {} CON: {} INT: {} WIS: {} CHA: {} HP: {}/{}' \
            .format(self.strength, self.dexterity, self.constitution,
                    self.intelligence, self.wisdom, self.charisma, self.hp, self.max_hp)

    def equip(self, itemid):
        return 0
