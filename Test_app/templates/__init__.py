from flask import Flask,g,make_response,Response,request,render_template,session
from datetime import timedelta
# Application 객체 생성
app =Flask(__name__)
# 좀 더 세밀한 에러까지 나게 해줌.
app.debug = True

app.config.update(
    SECRET_KEY = 'X1243yRH!mMwf',
    SESSION_COOKIE_NAME  = 'pyweb_flask_session',
    PERMANENT_SESSION_LIFETIME = timedelta(31)
)

### route parameter

@app.route("/tmpl")
def t():
    title = request.args.get('title')
    return render_template("jinja.html",title = title)

@app.route('/test')
def test():
    return render_template("yy.html")

@app.route('/portfolio/yy.html',methods = ['POST','GET'])
def post():
    List = []
    for i in range(1,6) :
        parameter = "Test" + str(i)
        value = request.form[parameter]
        String = 'Test'+str(value)
        print(String)
        List.append(String)
    return ",".join(List)

# write cookie
@app.route('/wc')
def Init() :
    key = request.args.get('key')
    val = request.args.get('val')
    res = Response('SET COOKIE')
    res.set_cookie(key,val)
    session['Token'] = '123X'
    return make_response(res)


@app.route('/show_result')
def show_result() :
    return 'pass'

