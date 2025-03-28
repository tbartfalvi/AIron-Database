import certifi
from pymongo.mongo_client import MongoClient
from airondatarepository import dataconstants
from airondatarepository.user import User

# The mongodb user repository
class UserRepository:
    def __init__(self):
        pass

    def insert_user(self, user: User):
        try:
            client = MongoClient(dataconstants.CONNECTION_STRING, tlsCAFile=certifi.where())
            db = client[dataconstants.DB_NAME]
            col  = db[dataconstants.USER_COLLECTION]
            new_user = col.insert_one({ dataconstants.FULL_NAME: user.full_name, dataconstants.EMAIL: user.email, dataconstants.PASSWORD: user.password })
            id = new_user.inserted_id
            client.close()
            return id
        except Exception as e:
            print("An exception occurred ::", e)
            return -9999
    
    def user_exsits(self, email: str):
        client = MongoClient(dataconstants.CONNECTION_STRING, tlsCAFile=certifi.where())
        db = client[dataconstants.DB_NAME]
        col  = db[dataconstants.USER_COLLECTION]
        query = { dataconstants.EMAIL: email }
        doc = col.find(query)
        client.close()
        for x in doc:
            if x == email:
                return True
            
        return False
    
    def delete_user(self, email: str):
        client = MongoClient(dataconstants.CONNECTION_STRING, tlsCAFile=certifi.where())
        db = client[dataconstants.DB_NAME]
        col  = db[dataconstants.USER_COLLECTION]
        query = { dataconstants.EMAIL: email }
        result = col.delete_one(query)
        return result.deleted_count > 0