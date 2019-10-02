from flask import Flask,g

app =Flask(__name__)
app.debug = True

@app.before_first_request
def before_request():
    print("before_request!!")
    # 서버를 제어하고 싶을때 주로 사용됨.
    g.str = '한글'

@app.route("/gg")
def helloworld():
    return "hello Flask World!" + getattr(g,'str','111')

@app.route("/")
def helloworld2():
    return "hello Flask World!"

