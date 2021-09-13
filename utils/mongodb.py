import pymongo
from config import config

class MongoDB:
    def __init__(self):
        self.client = pymongo.MongoClient(config.mongodb_uri)
        self.db = self.client.get_database()
        print(self.client)

    def insert(self, collection, data):
        return self.db[collection].insert(data)

    def find(self, collection, query):
        return self.db[collection].find(query)

    def find_one(self, collection, query):
        return self.db[collection].find_one(query)

    def update(self, collection, query, data):
        return self.db[collection].update(query, data)

    def delete(self, collection, query):
        return self.db[collection].delete_one(query)

    def drop(self, collection):
        return self.db[collection].drop()