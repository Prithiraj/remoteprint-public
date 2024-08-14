import enum
from json import loads
from os.path import dirname

dir_path = dirname(__file__) 

class DBTypes(enum.Enum):
    postgresql = 1
    mysql = 2

class Credentials(object):
    def __init__(self, dbtype):
        
        creds = ""
        with open(dir_path + "/credentials.json", 'r') as f:
            creds = loads(f.read())[dbtype]
        
        self.sqlalchemy = creds["sqlalchemy"]
        self.host = creds["host"]
        self.port = creds["port"]
        self.database = creds["database"]
        self.user = creds["user"]
        self.password = creds["password"]
