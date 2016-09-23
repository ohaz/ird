from database import Base
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

__author__ = 'ohaz'

room_transit = Table('room_transit', Base.metadata,
    Column('entry_id', Integer, ForeignKey('room.id'), primary_key=True),
    Column('exit_id', Integer, ForeignKey('room.id'), primary_key=True),
    Column('oneway', Boolean(), default=False)
)

class Room(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True)
    desc_name = Column(String(32))
    desc_flavor = Column(String(192))
    generated = Column(Boolean(), default=False)
    exits = relationship("Room", secondary=room_transit, primaryjoin=id==room_transit.c.entry_id, secondaryjoin=id==room_transit.c.exit_id, backref="entries")

    characters = relationship("Character", back_populates="room")

    def get_description(self):
        exitList = ""
        for exitIt in self.exits:
            exitList += ", [{}] {}".format(exitIt.id, exitIt.desc_name)
        return "You are {}. {} Exits: {}.".format(self.desc_name, self.desc_flavor, exitList[2:])

    def __str__(self):
        exitlist = ""
        if len(self.exits) > 1:
            existlist = str(self.exits[0].id)
            for exitIt in self.exits[1:]:
                exitlist += ", " + str(exitIt.id)
        elif len(self.exits) == 1:
            existlist = str(self.exits[0].id)
        return '<Room {}, \'{}\', \'{}\',  [{}]>'.format(self.id, self.desc_name, self.desc_flavor, existlist)

    def __repr__(self):
        return str(self)
