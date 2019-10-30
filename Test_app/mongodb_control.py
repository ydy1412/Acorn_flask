from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
databases = client.list_database_names()
db = client.get_database("member")
collections = db.get_collection('Account')
login_data = {"id": 'ydy1412',"password" : '920910'}
Id_existence = collections.find_one(login_data)
print(Id_existence)
# data = {"author" : "Mike",'text' : "my first blog post!"}
# collect.insert_one(data)
# Str = ""
# for i in collect.find() :
#     Str += str(i)
client.close()