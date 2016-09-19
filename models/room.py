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
    generated = Column(Boolean(), default=False)
    exits = relationship("Room", secondary=room_transit, primaryjoin=id==room_transit.c.entry_id, secondaryjoin=id==room_transit.c.exit_id, backref="entries")
    users = relationship('User')

    def __str__(self):
        return 'BLA'
        return '<Room {}, neighbours: {}>'.format(self.id, [exits.id for exit in self.exits])

    def __repr__(self):
        return str(self)
