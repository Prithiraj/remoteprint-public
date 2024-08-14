# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, create_engine, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from configurations.configurations import Credentials, DBTypes

Base = declarative_base()
metadata = Base.metadata


class Queue(Base):
    __tablename__ = 'queues'

    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(255))
    position = Column(Integer, nullable=False, server_default=text("1"))
    header = Column(Text)
    footer = Column(Text)
    logo = Column(String(255))
    coupon = Column(String(255))


class Device(Base):
    __tablename__ = 'devices'

    devicemac = Column(String(50), primary_key=True)
    queue_id = Column(ForeignKey('queues.id'))
    dot_width = Column(Integer)
    status = Column(String(50))
    client_type = Column(String(255))
    client_version = Column(String(255))
    printing = Column(Integer)
    last_poll = Column(DateTime(True))

    queue = relationship('Queue')

dbtype = DBTypes.mysql.name
creds = Credentials(dbtype)

db_string = f"{creds.sqlalchemy}://{creds.user}:{creds.password}@{creds.host}:{creds.port}/{creds.database}"
engine = create_engine(db_string, convert_unicode=True)
metadata.create_all(engine, checkfirst=True)