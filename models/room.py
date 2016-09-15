from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

__author__ = 'ohaz'


class Room(Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True)
    generated = Column(Boolean(), default=False)
    parent_id = Column(Integer, ForeignKey('room.id'))
    parent = relationship('Room', back_populates='children', remote_side=[id])
    children = relationship('Room', back_populates='parent')
    users = relationship('User')

    def __str__(self):
        return '<Room {}, neighbours: {}>'.format(self.id, [self.parent.id if self.parent else None]+[child.id for child in self.children])

    def __repr__(self):
        return str(self)
