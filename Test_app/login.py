from flask import Flask,g,make_response,Response,request,render_template,session
from pymongo import MongoClient

app =Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8zdkjsfhqw]/'

client = MongoClient('mongodb://localhost:27017')
if "member" not in client.list_database_names() :
    db = client['member']
    collect = db['Account']
    data = {'id': 'ydy1412', 'password': '920910'}
    collect.insert_one(data)
    client.close()
else :
    client.close()

@app.route("/")
def helloworld2():
    return render_template('main_page.html')

@app.route("/home")
def home():
    return "home"

@app.route("/Portpolio")
def portpolio():
    return "Portpolio"

@app.route("/team_info")
def team_info():
    return "team_info"

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/member_checked",methods = ['POST'])
def member_checked():
    id = request.form['id']
    password = request.form['password']
    client = MongoClient('mongodb://localhost:27017')
    db = client['member']
    collect = db['Account']
    login_data = {"id": str(id),"password" : str(password)}
    Id_existence = collect.find_one(login_data)
    client.close()
    if Id_existence is not None :
        return render_template('main_page.html')
    else :
        return "no id"


if __name__ == "__main__" :
    app.debug = True
    app.run(host = "0.0.0.0")
