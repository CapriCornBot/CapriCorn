import logging
from config import config


import mysql.connector
from mysql.connector import cursor as curs

log = logging.getLogger(config.bot_name)

class Database:
    def __init__(self, client) -> None:
        """Init Database
        """
        self.client = client
        import mysql.connector
        from mysql.connector import cursor as curs
        # get credits from environment variables
        self.db_config = {
            'user': config.mysql_user,
            'password': config.mysql_password,
            'host': config.mysql_host,
            'port': config.mysql_port,
            'database': config.mysql_db,
            'buffered': True
        }
        self.connection: mysql.connector.MySQLConnection = None
        self.cursor: curs.MySQLCursorBuffered = None
    
    def connect(self) -> None:
        """Connect to databse"""
        self.connection = mysql.connector.connect(user=config.mysql_user, password=config.mysql_password, host=config.mysql_host, port=config.mysql_port, database=config.mysql_db, buffered=True)
        self.connection.autocommit = True
        self.cursor: curs.MySQLCursorBuffered = self.connection.cursor(dictionary=True)
        log.info('Connected to database')
        self.client.dispatch("mysql_connected")
    
    def disconnect(self) -> None:
        """Disconnects"""
        try: 
            self.cursor.close()
        except AttributeError:
            pass
        try:
            self.connection.close()
        except AttributeError:
            pass
    
    def check_connection(self) -> bool:
        if self.connection is None:
            return False
        if self.connection.is_connected():
            return True
        return False


    def execute(self, query: str, params: dict = None) -> None:
        self.cursor.execute(query, params)
    
    def fetchone(self) -> dict:
        return self.cursor.fetchone()
    
    def fetchall(self) -> list:
        return self.cursor.fetchall()
    
    def commit(self) -> None:
        self.connection.commit()
    
    def rollback(self) -> None:
        self.connection.rollback()
    
    def __enter__(self) -> 'Database':
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.disconnect()
    
    def __del__(self) -> None:
        self.disconnect()
    
    