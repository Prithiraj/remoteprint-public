import logging
from contextlib import contextmanager

import psycopg2
import psycopg2.extras
# from db_manager import credentials
from app_ver_2.configurations.configurations import Credentials

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class DBConnection(object):
    def __init__(self):

        credentials = Credentials()
        try:
            self.conn = psycopg2.connect(
                host=credentials.host,
                port=credentials.port,
                database=credentials.database,
                user=credentials.user,
                password=credentials.password
            )

            self.conn.autocommit = True
            
            self.dict_cursor = self.conn.cursor(
                cursor_factory = psycopg2.extras.RealDictCursor
            )

        except Exception as e:
            print(e.args)
    
    def done(self):
        self.dict_cursor.close()
        print('cursor got closed')
        if self.conn is not None:
            self.conn.close()
            print('Connection is closed')

@contextmanager
def dbConnection():
    connection = DBConnection()
    try:
        yield connection
    finally:
        connection.done()

if __name__ == "__main__":
    dbConn = DBConnection()
    dbConn.done()
