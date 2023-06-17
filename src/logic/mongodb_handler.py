import pymongo
import uuid
from logic.logging_handler import logger


class Mongo:
    def __init__(self):
        self.dyn_server = None
        self.dyn_db = None
        self.dyn_collection = None

    def user_db_handler(self, steamid, server, db, collection):
        self.dyn_server = server
        self.dyn_db = db
        self.dyn_collection = collection
        try:
            client = pymongo.MongoClient(self.dyn_server)
            self.dyn_db = client[self.dyn_db]
            self.dyn_collection = self.dyn_db[self.dyn_collection]

            existing_document = self.dyn_collection.find_one({'steamid': steamid})

            if existing_document:
                print(f"Document with steamid {steamid} already exists.")
                userId = existing_document['userId']
                token = existing_document['token']
                return userId, token
            else:
                userId = str(uuid.uuid4())
                token = str(uuid.uuid4())

                new_document = {
                    'steamid': steamid,
                    'userId': userId,
                    'token': token
                }

                self.dyn_collection.insert_one(new_document)
                logger.graylog_logger(level="info", handler="mongodb", message=f"New user added to database: {steamid}")
                return userId, token
        except Exception as e:
            logger.graylog_logger(level="error", handler="mongodb", message=f"Error in mongodb_handler: {e}")
            return None, None

    def get_user_info(self, userId, server, db, collection):
        try:
            self.dyn_server = server
            self.dyn_db = db
            self.dyn_collection = collection
            client = pymongo.MongoClient(self.dyn_server)
            self.dyn_db = client[self.dyn_db]
            self.dyn_collection = self.dyn_db[self.dyn_collection]
            existing_document = self.dyn_collection.find_one({'userId': userId})

            if existing_document:
                steamid = existing_document['steamid']
                token = existing_document['token']
                return steamid, token
            else:
                print(f"No user found with userId: {userId}")
                return None, None
        except Exception as e:
            print(e)
            return None, None


mongo = Mongo()