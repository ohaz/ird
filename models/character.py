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
        self.strength       = stats[0]
        self.dexterity      = stats[1]
        self.constitution   = stats[2]
        self.intelligence   = stats[3]
        self.wisdom         = stats[4]
        self.charisma       = stats[5]

        self.max_hp = 20 + 3 * self.constitution
        self.hp = self.max_hp


    def print_stats(self):
        return 'STR: {} DEX: {} CON: {} INT: {} WIS: {} CHA: {} HP: {}/{}' \
            .format(self.strength, self.dexterity, self.constitution,
                    self.intelligence, self.wisdom, self.charisma, self.hp, self.max_hp)