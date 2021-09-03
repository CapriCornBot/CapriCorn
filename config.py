import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        pass
    
    @property
    def bot_name(self):
        load_dotenv()
        print("bot_name ist", os.getenv('BOT_NAME'))
        return os.getenv('BOT_NAME')

    @property
    def mysql_host(self):
        load_dotenv()
        return os.getenv('MYSQL_HOST')
    
    @property
    def mysql_user(self):
        load_dotenv()
        return os.getenv('MYSQL_USERNAME')
    
    @property
    def mysql_password(self):
        load_dotenv()
        return os.getenv('MYSQL_PASSWORD')
    
    @property
    def mysql_db(self):
        load_dotenv()
        return os.getenv('MYSQL_DB')
    @property
    def mysql_port(self):
        load_dotenv()
        return os.getenv('MYSQL_PORT')


config = Config()