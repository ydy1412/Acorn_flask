from pymongo import MongoClient
import sys
def create_account(id,password) :
    client = MongoClient("mongodb://localhost:27017/")
    databases = client.list_database_names()
    db = client.get_database("member")
    collections = db.get_collection('Account')
    login_data = {"id": id, "password": password}
    Id_existence = collections.find_one(login_data)
    if Id_existence == True:
        print("Id is already existed")
    else :
        collections.insert_one(login_data)
        print("Id created")
    client.close()

if __name__ == "__main__" :
    create_account(sys.argv[1],sys.argv[2])

