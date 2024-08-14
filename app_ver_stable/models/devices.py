# coding: utf-8
from datetime import datetime

from app_ver_stable.models.queues import Queue
from app_ver_stable.utilities.validate import Validate
from app_ver_stable.dbmanager.database import Base
from app_ver_stable.dbmanager.database import db_session as db
from app_ver_stable.dbmanager.database import dbtype, session_manager
from sqlalchemy import (TIMESTAMP, Column, DateTime, ForeignKey, Integer,
                        String, Text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class Device(Base):
    
    if dbtype == "postgresql":
        __tablename__ = 'devices'
        devicemac = Column(String, primary_key=True)
        queue_id = Column(ForeignKey('queues.id'))
        markup = Column(Text)
        dot_width = Column(Integer)
        status = Column(String)
        client_type = Column(String)
        client_version = Column(String)
        printing = Column(Integer)
        last_poll = Column(DateTime(True))

        queue = relationship('Queue')
    
    if dbtype == "mysql":
        __tablename__ = 'devices'

        devicemac = Column(String(50), primary_key=True)
        queue_id = Column(ForeignKey('queues.id'))
        markup = Column(Text)
        dot_width = Column(Integer)
        status = Column(String(50))
        client_type = Column(String(255))
        client_version = Column(String(255))
        printing = Column(Integer)
        last_poll = Column(TIMESTAMP)

        queue = relationship('Queue')    

    def save_to_db(self):
        db.add(self)
        db.flush()
        id = self.devicemac
        db.commit()
        db.close()
        return id

    def update(self, **kwargs):
        mapped_values = {}
        for item in Device.__table__.columns:
            field_name = item.key
            if item.primary_key is False and field_name in kwargs:
                mapped_values[field_name] = kwargs[field_name]

        data = db.query(Device).filter(Device.devicemac ==
                                       self.devicemac).update(mapped_values)
        db.commit()
        db.close()
        return data

    @classmethod
    def addDevice(cls, deviceMac, queueId):
        try:
            Validate.isValidString(deviceMac)
            Validate.isDigit(queueId)
            newDevice = cls(
                devicemac=deviceMac,
                queue_id=queueId
            )
            id = newDevice.save_to_db()
            return id
        except ValueError:
            raise ValueError("invalid data provided")
        except Exception as e:
            print(e)

    @classmethod
    def delDevice(cls, deviceMac):
        try:
            Validate.isValidString(deviceMac)
            rowCount = cls.query.filter_by(devicemac=deviceMac).delete()
            db.commit()
            db.close()
            return rowCount
        except ValueError:
            raise ValueError("invalid data provided")

    @classmethod
    def getDeviceMarkup(cls, mac_id):
        # SELECT Printing, QueueID, DotWidth FROM Devices WHERE DeviceMac = '".$mac."'"
        try:
            Validate.isValidString(mac_id)
            result = ""
            with session_manager() as session:
                result = session.query().with_entities(
                    cls.markup, cls.queue_id, cls.dot_width
                ).filter(
                    cls.devicemac == mac_id
                )
            return result.first()
        except ValueError:
            raise ValueError("invalid value provided")
        except Exception as e:
            print(e)

    @classmethod
    def getDevicePrintRequired(cls, mac_id):
        # SELECT Printing, QueueID, DotWidth FROM Devices WHERE DeviceMac = '".$mac."'"
        try:
            Validate.isValidString(mac_id)
            result = ""
            with session_manager() as session:
                result = session.query().with_entities(
                    cls.printing, cls.queue_id, cls.dot_width
                ).filter(
                    cls.devicemac == mac_id
                )
            return result.first()
        except ValueError:
            raise ValueError("invalid value provided")
        except Exception as e:
            print(e)

    @classmethod
    def getQueueIDandPrintingState(cls, mac_id):
        # "SELECT QueueID, Printing FROM Devices WHERE DeviceMac = '".$mac."'"
        try:
            Validate.isValidString(mac_id)
            result = ""
            with session_manager() as session:
                result = session.query().with_entities(
                    cls.queue_id, cls.printing, cls.dot_width
                ).filter(
                    cls.devicemac == mac_id
                )
            return result.first()
        except ValueError:
            raise ValueError("invalid value provided")
        except Exception as e:
            print(e)

    @classmethod
    def getDeviceOutputWidth(cls, mac_id):
        # SELECT DotWidth FROM Devices WHERE DeviceMac = '".$mac."'"
        try:
            Validate.isValidString(mac_id)
            result = ""
            with session_manager() as session:
                result = session.query().with_entities(
                    cls.dot_width
                ).filter(cls.devicemac == mac_id)
            return result.first()
        except ValueError:
            raise ValueError("invalid value provided")
        except Exception as e:
            return e

    @classmethod
    def setDeviceInfo(cls, devicemac, dot_width=None, clientType=None, clientVer=None):
        # "UPDATE Devices SET 'DotWidth' = '".$width."', 'ClientType' = '".$clientType."', 'ClientVersion' = '" .$clientVer."' WHERE DeviceMac = '" .$mac."';"
        try:
            Validate.isValidString(devicemac)
            data = cls(devicemac=devicemac).update(dot_width=dot_width,
                                                   client_type=clientType, 
                                                   client_version=clientVer, 
                                                   last_poll=datetime.utcnow())
            return data
        except ValueError:
            raise ValueError("invalid value provided")
        except Exception as e:
            raise e

    @classmethod
    def setDeviceStatus(cls, devicemac, status):
        try:
            Validate.isValidString(devicemac)
            # Validate.isValidString(status)
            data = cls(devicemac=devicemac).update(status=status)
            return data
        except ValueError:
            raise ValueError("invalid value provided")
        except Exception as e:
            raise e

    @classmethod
    def setCompleteJob(cls, devicemac):
        try:
            Validate.isValidString(devicemac)
            data = cls(devicemac=devicemac).update(printing=0)
            return data
        except ValueError:
            raise ValueError("invalid value provided")
        except Exception as e:
            raise e

    @classmethod
    def listDevices(cls):
        # $results = $db->query("SELECT DeviceMac, Status, QueueID, Queues.name, ClientType, ClientVersion, LastPoll FROM Devices INNER JOIN Queues ON Queues.id = Devices.QueueID")
        result = []
        try:
            with session_manager() as session:
                result = session.query(
                    Queue, cls).join(
                        Queue, Queue.id == cls.queue_id
                ).with_entities(
                        cls.devicemac, 
                        cls.status, 
                        cls.queue_id, 
                        Queue.name.label("queue_name"), 
                        cls.client_type, 
                        cls.client_version, 
                        cls.last_poll
                ).all()

                if bool(result) is False:
                    result = []
                return result
        except Exception as e:
            return False

    @classmethod
    def setDevicePrinting(cls, devicemac, printing=0):
        try:
            Validate.isValidString(devicemac)
            Validate.isDigit(printing, min_allowed=0)
            data = cls(devicemac=devicemac).update(printing=printing)
            return data
        except ValueError:
            raise ValueError("Invalid device position")
        except Exception as e:
            print(e)
