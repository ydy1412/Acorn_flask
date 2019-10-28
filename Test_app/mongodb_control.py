from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
databases = client.list_database_names()
print(databases)
client.drop_database("testdb")
databases = client.list_database_names()
print(databases)
# db = client.get_database("testdb")
# collect = db.get_collection("people")
# data = {"author" : "Mike",'text' : "my first blog post!"}
# collect.insert_one(data)
# Str = ""
# for i in collect.find() :
#     Str += str(i)
client.close()