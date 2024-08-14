from contextlib import contextmanager

from app_ver_1.configurations.configurations import Credentials, DBTypes
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative, declarative_base
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import scoped_session, sessionmaker

# dbtype = DBTypes.postgresql.name
dbtype = DBTypes.mysql.name
creds = Credentials(dbtype)
# db_string = f"postgresql://{creds.user}:{creds.password}@{creds.host}:{creds.port}/{creds.database}"

db_string = f"{creds.sqlalchemy}://{creds.user}:{creds.password}@{creds.host}:{creds.port}/{creds.database}?charset=utf8mb4"
# print(db_string)

engine = create_engine(db_string, pool_size=48, max_overflow=68)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=True,
                                         bind=engine))

# Base = declarative_base()

@as_declarative()
class Base:
    def _asdict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

Base.query = db_session.query_property()

# def init_db():
#     print("init_db called")
#     from core.models.member_invitation import MemberInvitation
#     Base.metadata.create_all(bind=engine)

@contextmanager
def session_manager():
    try:
        yield db_session
        db_session.commit()
    except Exception as e:
        db_session.rollback()
    finally:
        db_session.remove()
        db_session.close() 
