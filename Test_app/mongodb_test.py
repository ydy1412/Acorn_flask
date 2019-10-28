from pymongo import MongoClient
client = MongoClient()
print(client.list_database_names())
db = client['member']
collect =  db['Account']
# data = {'id':'ydy1412','password' : '920910'}
# collect.insert_one(data)
print(collect.find_one({"id": 'ydy1412',"password" : '1111'}))

client.close()