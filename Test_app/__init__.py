from flask import Flask,g,make_response,Response,request,render_template
from datetime import datetime,date
import requests

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

# Application 객체 생성
app =Flask(__name__)

# 좀 더 세밀한 에러까지 나게 해줌.
app.debug = True
### route parameter

@app.route('/res1')
def res1():
    custom_res = Response("Custom Response",201,{'test':'ttt'})
    # 헤더를({'test' : 'ttt'}) 보내고 싶을땐 dict형으로 전송
    return getattr(g,'str','111')
    # make_response는 데이터를 stream 형태로 전송함.

@app.route("/login")
def login() :
    return render_template("Login.html")

# before_first_request : 사용자가 처음 사이트에 접속하여 request를 보내자마자 실행되는 함수
# before_request : 사용자가 같은 사이트에 있더라도 request(F5)를 보내면 실행되는함수. (보통 web filter에 사용됨)
# - web filter : euc-kr 를 utf 로 변환해 주는 등 전처리를 하는 작업.
# after_request : response를 하기 직전에 시행되는 함수 ( 보통 db를 닫는 용도로 사용됨)
# teardown_request : str이 모두 완료된 후 실행 ( 오류 처리 필수 ) - 돈이 제대로 전송되지 않았을 시 에러를 처리하기 위함.
# teardown_appcontext : app이 모두 완료된 후 실행 ( 오류 처리 필수 )
@app.before_request
def before_request():
    print("before_request!!")
    # 서버를 제어하고 싶을때 주로 사용됨.
    g.str = '한글'

@app.before_first_request
def before_request():
    print("first_request!!")
    # 서버를 제어하고 싶을때 주로 사용됨.

# url을 통해 백엔드에 들어오는 데이터를 유동적으로 받을 수 있음.
@app.route('/test/<tid>')
def test3(tid) :
    print("tid is",tid)
    return "hello Flask World!"

# 다음과 같이 url default 값을 줄 수가 있음.
@app.route('/test2',defaults ={'page':'index'})
@app.route('/test2/<page>')
def printpage(page) :
    return str(page)

# redirect homepage 설정 방법.
@app.route('/test3', host ='abc.com')
@app.route('/test3', redirect_to = '/new_test' )
def redirectpage(page) :
    return str(page)

# @app.route("/gg")
# def helloworld():
#     return "hello Flask World!" + getattr(g,'str','111')

# WSGI(Webserver Gateway Interface)
@app.route('/test_wsgi')
def wsgi_test():
    def application(environ, start_response) :
        # environ은 flask의 환경변수를 담고있는 dict형 객체
        body = 'The Request method was %s' % environ['REQUEST_METHOD']
        headers = [('Content-Type','text/plain'),('Content-Length',str(len(body)))]
        # text/plain은 html과 다름.
        start_response('200 OK', headers)
        return [body]
    # application 함수는 start_response func와 environ dict를 인수로 받음.
    # body를 적절한 형태의 str으로 변형한 뒤 header의 값을 형성.
    # header에는 content-type와 content-length 데이터를 넣어서 전송.
    # start_response의 인수에 header를 넣어서 실행 시킨 뒤 [body] 를 반환.
    # make_response는 [body]를 stream의 형태로 전송(image와 같은 파일)
    return make_response(application)

@app.route("/")
def helloworld2():
    return "hello Flask World!"

######## request parameter
#/rpargs?v=한글 => q = 한글 이라고나옴.
# => 장점 : 빠름.
# => 단점 : 데이터의 양이 한정적임(1024byte)
@app.route('/rpargs')
def rpargs() :
    q = request.args.get('v')
    if str(q) == "한글":
        templates = "Application.html"
    else :
        templates = 'post.html'
    return render_template(templates)

#/rppost?v=한글 => q = 한글 이라고나옴.
# => 장점 : 데이터를 무한정 보낼 수 있음
# => 단점 : 느림
@app.route('/rppost')
def rppost() :
    q = request.form.get('v')

    if str(q) == "한글":
        templates = "Application.html"
    else :
        templates = 'post.html'
    return render_template(templates)

#/rpvalues?v=한글 => q = 한글 이라고나옴.
# => 장점 : 편함
# => 단점 : 컴퓨터에 부담을 줌
@app.route('/rpvalues')
def rpvalues() :
    q = request.values.get('v')
    return "q= %s" % str(q)

#/rpl?v=한글,영어라고 url을 치면 q = ['한글','영어']라고 출력되서 나옴.
@app.route('/rpl')
def rpl() :
    q = request.values.getlist('v')
    return "q= %s" % str(q)

# request 처리 용 함수
def ymd(fmt):
    def trans(date_str) :
        return datetime.strptime(date_str,fmt)
    return trans

@app.route('/dt')
def dt() :
    # /dt?date = 2019-08-02 라고 주면 -> 우리나라 시간 형식 :2019-08-02 00:00:00
    # /dt만 주어지면 data.today()를 표현. => 우리나라 시간 형식 :2019-10-08
    # 함수에 함수를 넣는 이유는 안쓰는 함수는 만들지 않고 쓰는 함수는 한번만 만들면 계속 사용할 수 있기 때문이란다.
    datestr = request.values.get('date',date.today(), type = ymd("%Y-%m-%d"))
    return "우리나라 시간 형식 :" + str(datestr)

if __name__ == "main" :
    app.run(host='0.0.0.0')

