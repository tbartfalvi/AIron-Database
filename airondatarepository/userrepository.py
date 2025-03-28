import pymongo
from airondatarepository import dataconstants
from airondatarepository.user import User

# The mongodb user repository
class UserRepository:
    def __init__(self):
        pass

    def insert_user(self, user: User):
        try:
            client = pymongo.MongoClient(dataconstants.CONNECTION_STRING)
            db = client[dataconstants.DB_NAME]
            col  = db[dataconstants.USER_COLLECTION]
            new_user = col.insert_one({ dataconstants.FULL_NAME: user.full_name, dataconstants.EMAIL: user.email, dataconstants.PASSWORD: user.password })
            id = new_user.__inserted_id
            client.close()
            return id
        except Exception as e:
            print("An exception occurred ::", e)
            return -9999
    
    def user_exsits(self, email: str):
        client = pymongo.MongoClient(dataconstants.CONNECTION_STRING)
        db = client[dataconstants.DB_NAME]
        col  = db[dataconstants.USER_COLLECTION]
        query = { dataconstants.EMAIL: email }
        doc = col.find(query)
        client.close()
        for x in doc:
            if x == email:
                return True
            
        return False
    
    def delete_user(self, _id):
        client = pymongo.MongoClient(dataconstants.CONNECTION_STRING)
        db = client[dataconstants.DB_NAME]
        col  = db[dataconstants.USER_COLLECTION]
        query = { dataconstants.ID: _id }
        col.delete_one(query)