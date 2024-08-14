# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Queue(Base):
    __tablename__ = 'queues'

    id = Column(Integer, primary_key=True, server_default=text("nextval('queues_id_seq'::regclass)"))
    name = Column(String)
    position = Column(Integer)
    header = Column(Text)
    footer = Column(Text)
    logo = Column(String)
    coupon = Column(String)


class Device(Base):
    __tablename__ = 'devices'

    devicemac = Column(String, primary_key=True)
    queue_id = Column(ForeignKey('queues.id'))
    dot_width = Column(Integer)
    status = Column(String)
    client_type = Column(String)
    client_version = Column(String)
    printing = Column(Integer)
    last_poll = Column(DateTime(True))

    queue = relationship('Queue')
