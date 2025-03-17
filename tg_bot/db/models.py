from datetime import datetime

from sqlalchemy import Column, Integer, BigInteger, VARCHAR, DateTime, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger)
    card_number = Column(VARCHAR)
    card_name = Column(VARCHAR)

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    api_uuid = Column(VARCHAR)
    url = Column(Text)
    amount = Column(Integer)
    user_tid = Column(BigInteger)
    card_number = Column(VARCHAR)
    status = Column(VARCHAR, default='active')
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
