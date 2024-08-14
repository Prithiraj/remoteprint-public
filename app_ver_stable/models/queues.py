# coding: utf-8
from app_ver_stable.dbmanager.database import Base
from app_ver_stable.dbmanager.database import db_session as db
from app_ver_stable.dbmanager.database import dbtype, session_manager
from sqlalchemy import Column, ForeignKey, Integer, String, Text, false, text
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine.row import Row
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app_ver_stable.starmarkupengine.tags import DrawerOpenModes
from app_ver_stable.utilities.validate import Validate

# Base = declarative_base()
# metadata = Base.metadata


class Queue(Base):
    if dbtype == "postgresql":
        __tablename__ = 'queues'

        id = Column(Integer, primary_key=True, server_default=text("nextval('queues_id_seq'::regclass)"))
        name = Column(String)
        position = Column(Integer, nullable=False, server_default=text("1"))
        markup = Column(Text)
        header = Column(Text)
        footer = Column(Text)
        logo = Column(String)
        coupon = Column(String)
        drawer_open_at = Column(String)
        buzzers_at_start = Column(Integer)
        buzzers_at_end = Column(Integer)

    if dbtype == "mysql":
        __tablename__ = 'queues'

        id = Column(Integer, primary_key=True, autoincrement="auto")
        name = Column(String(255))
        position = Column(Integer, nullable=False, server_default=text("1"))
        markup = Column(Text)
        header = Column(Text)
        footer = Column(Text)
        logo = Column(String(255))
        coupon = Column(String(255))
        drawer_open_at = Column(String(100))
        buzzers_at_start = Column(Integer)
        buzzers_at_end = Column(Integer) 
        
    def save_to_db(self):
        db.add(self)
        db.flush()
        id = self.id
        db.commit()
        db.close()
        return id
    
    def update(self, **kwargs):
        mapped_values = {} 
        for item in Queue.__table__.columns:
            field_name = item.key
            if item.primary_key is False and field_name in kwargs:
                mapped_values[field_name] = kwargs[field_name] 
        q = db.query(Queue).filter(Queue.id==self.id).update(mapped_values)
        db.commit()
        db.close()
        return q
    
    @classmethod
    def getQueuePrintParameters(cls, queue_id):
        try:
            ## SELECT Header, Footer, Logo, Coupon FROM Queues WHERE id = '" .$queue."'"
            Validate.isDigit(queue_id)
            result = ""
            with session_manager() as session:
                result = session.query().with_entities(
                        cls.header, 
                        cls.footer, 
                        cls.logo, 
                        cls.coupon, 
                        cls.markup, 
                        cls.drawer_open_at, 
                        cls.buzzers_at_start, 
                        cls.buzzers_at_end
                    ).filter(
                    cls.id == queue_id
                )
            return result.first()
        except ValueError:
            raise ValueError("Invalid value provided")
        except Exception as e:
            print(e)

    
    @classmethod
    def getPosition(cls, queueId):
        try:
            Validate.isDigit(queueId)
            
            with session_manager() as session:
                result = session.query().with_entities(
                    cls.position
                ).filter(cls.id==queueId).scalar()
            return result
        except ValueError:
            raise ValueError("invalid value provider")
        except Exception as e:
            raise e.message

    @classmethod
    def updatePosition(cls, queueId: int, markup: str, drawer_open_at: str = DrawerOpenModes.START.name , buzzers_at_start: int = 0, buzzers_at_end: int = 0):
        # "UPDATE Queues SET position = position + 1 WHERE id = '".$queue."'"
        try:
            Validate.isDigit(queueId)
            
            with session_manager() as session:
                result = session.query(cls).filter(cls.id==queueId).update(
                    {'position': cls.position + 1, 
                     'markup': markup, 
                     'drawer_open_at': drawer_open_at,
                     'buzzers_at_start': buzzers_at_start,
                     'buzzers_at_end': buzzers_at_end})
                db.commit()
                # print("Here is the data " + str(result.statement.compile(dialect=postgresql.dialect())))
                return result
        except ValueError:
            raise ValueError("invalid value provided")
        except Exception as e:
            return e 
        
    @classmethod
    def addQueue(cls, name: str):
        # "INSERT INTO `Queues`(name) VALUES ('".$name."');"
        name = name.strip()
        if name is None or name=="":
            raise ValueError('invalid value provided')
        try:
            newQueue = cls(
                name=name
            )
            id = newQueue.save_to_db()
            return id
        except Exception as e:
            print(e)
            
    @classmethod
    def delQueue(cls, queueId: int):
        # "DELETE FROM `Queues` WHERE `id`='".$id."';"
        try:
            Validate.isDigit(queueId)
            rowCount = cls.query.filter_by(id=queueId).delete()
            db.commit()
            db.close()
            return rowCount
        except ValueError:
            raise ValueError('invalid value provided') 
        except Exception as e:
            print(e.args)
        
    @classmethod
    def resetQueue(cls, queueId):
        try:
            Validate.isDigit(queueId)
            data = cls(id=queueId).update(position=1)
            return data
        except ValueError:
            raise ValueError('invalid value provided')
        except Exception as e:
            print(e)
            
    @classmethod
    def listQueues(cls):
        try:
            result = []
            with session_manager() as session:
                result = session.query().with_entities(
                    cls.id, 
                    cls.name, 
                    cls.position).all()
                if bool(result) is False:
                    result = []
                return result
        except Exception as e:
            print(e)
