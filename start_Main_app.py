### start_Main_app.py 는 실제 application을 구동시켜주는 프로그램임.
from Main_app import app
#from Test_app import app

# app.run(host='0.0.0.0') #127.0.0.1 == localhost(컴퓨터의 ip)
app.run(host='0.0.0.0') #127.0.0.1 == localhost(컴퓨터의 ip)