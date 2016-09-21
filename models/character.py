from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import utils
from database import Base

__author__ = 'Hamster'

class Character(Base):
    __tablename__ = 'character'
    id = Column(Integer, primary_key=True)
    user = relationship("User", uselist=False, back_populates="character")

    level = Column(Integer)
    hp = Column(Integer)
    max_hp = Column(Integer)
    strength = Column(Integer)
    dexterity = Column(Integer)
    constitution = Column(Integer)
    intelligence = Column(Integer)
    wisdom = Column(Integer)
    charisma = Column(Integer)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.roll_stats()


    def roll_stats(self):
        stats = utils.generate_stats(self.level)
        self.hp = stats[0]
        self.max_hp = self.hp
        self.strength = stats[1]
        self.dexterity = stats[2]
        self.constitution = stats[3]
        self.intelligence = stats[4]
        self.wisdom = stats[5]
        self.charisma = stats[6]

    def print_stats(self):
        return 'STR: {} DEX: {} CON: {} INT: {} WIS: {} CHA: {}' \
            .format(self.strength, self.dexterity, self.constitution,
                    self.intelligence, self.wisdom, self.charisma)