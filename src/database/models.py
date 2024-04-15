from sqlalchemy import Column, Integer, CHAR, ForeignKey, func, DateTime, Float, TIME
from sqlalchemy.dialects.mysql import FLOAT
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from db_connection import Base, engine


class CoinBid(Base, SerializerMixin):
    __tablename__ = 'Coin_bid'
    id = Column(Integer, primary_key=True, autoincrement=True)
    currency = Column(CHAR(36))
    time = Column(DateTime, default=func.now())
    price = Column(FLOAT(unsigned=True))


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine

    exit()
