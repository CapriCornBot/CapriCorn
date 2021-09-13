import os
from dotenv import load_dotenv
import urllib.parse
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
        return os.getenv('MYSQL_DATABASE')
    @property
    def mysql_port(self):
        load_dotenv()
        return os.getenv('MYSQL_PORT')

    @property
    def gateway_url(self):
        load_dotenv()
        return os.getenv('GATEWAY_URL')

    @property
    def webserver_url(self):
        load_dotenv()
        return os.getenv('WEBSERVER_URL')

    @property
    def mongodb_uri(self):
        load_dotenv()
        host = os.getenv('MONGODB_HOST')
        port = os.getenv('MONGODB_PORT')
        password = os.getenv('MONGODB_PASSWORD')
        username = os.getenv('MONGODB_USERNAME')
        db = os.getenv('MONGODB_DATABASE')
        #percent escape password and username
        # password = urllib.parse.quote_plus(password)
        # username = urllib.parse.quote_plus(username)
        print(host, port, password, username, db)
        return f"mongodb://{username}:{password}@{host}/{db}"
config = Config()