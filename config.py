import os
from dotenv import load_dotenv
import urllib.parse


class Config:
    def __init__(self):
        pass

    @property
    def bot_name(self):
        load_dotenv()
        return os.getenv('BOT_NAME')

    @property
    def mongodb_uri(self):
        load_dotenv()
        host = os.getenv('MONGODB_HOST')
        port = os.getenv('MONGODB_PORT')
        password = os.getenv('MONGODB_PASSWORD')
        username = os.getenv('MONGODB_USERNAME')
        db = os.getenv('MONGODB_DATABASE')
        # percent escape password and username
        # password = urllib.parse.quote_plus(password)
        # username = urllib.parse.quote_plus(username)
        # print(host, port, password, username, db)
        return f"mongodb://{username}:{password}@{host}/{db}"

    @property
    def version(self):
        return "0.0.1"


config = Config()
