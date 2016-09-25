from database import Base, session
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.room import Room
from models.character import Character
import hashlib
import time

from models.user import new_user
from utils import utils
from utils.equip_slot import EquipSlots

__author__ = 'TheWhiteLlama'


class TelegramUser(Base):
    __tablename__ = 'telegram_user'
    telegram_user_id = Column(Integer, primary_key=True)
    # CHILD-Parent one-to-one relationship to user
    user_name = Column(Integer, ForeignKey('user.user_name'))
    user = relationship('User')


def new_telegram_user(telegram_user_id):
    return TelegramUser(telegram_user_id=telegram_user_id)
