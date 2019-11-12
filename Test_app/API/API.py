import urllib.request
import json
from keras import backend as K
from flask import session, render_template, Markup
from keras.models import model_from_yaml

def recall(y_target, y_pred):
            y_target_yn = K.round(K.clip(y_target, 0, 1))  # 실제값을 0(Negative) 또는 1(Positive)로 설정한다
            y_pred_yn = K.round(K.clip(y_pred, 0, 1))  # 예측값을 0(Negative) 또는 1(Positive)로 설정한다

            # True Positive는 실제 값과 예측 값이 모두 1(Positive)인 경우이다
            count_true_positive = K.sum(y_target_yn * y_pred_yn)

            # (True Positive + False Negative) = 실제 값이 1(Positive) 전체
            count_true_positive_false_negative = K.sum(y_target_yn)

            # Recall =  (True Positive) / (True Positive + False Negative)
            # K.epsilon()는 'divide by zero error' 예방차원에서 작은 수를 더한다
            recall = count_true_positive / (count_true_positive_false_negative + K.epsilon())

            # return a single tensor value
            return recall



def precision( y_target, y_pred):
        # clip(t, clip_value_min, clip_value_max) : clip_value_min~clip_value_max 이외 가장자리를 깎아 낸다
        # round : 반올림한다
        y_pred_yn = K.round(K.clip(y_pred, 0, 1))  # 예측값을 0(Negative) 또는 1(Positive)로 설정한다
        y_target_yn = K.round(K.clip(y_target, 0, 1))  # 실제값을 0(Negative) 또는 1(Positive)로 설정한다

        # True Positive는 실제 값과 예측 값이 모두 1(Positive)인 경우이다
        count_true_positive = K.sum(y_target_yn * y_pred_yn)

        # (True Positive + False Positive) = 예측 값이 1(Positive) 전체
        count_true_positive_false_positive = K.sum(y_pred_yn)

        # Precision = (True Positive) / (True Positive + False Positive)
        # K.epsilon()는 'divide by zero error' 예방차원에서 작은 수를 더한다
        precision = count_true_positive / (count_true_positive_false_positive + K.epsilon())

        # return a single tensor value
        return precision

def f1score(y_target, y_pred):
        _recall = recall(y_target, y_pred)
        _precision = precision(y_target, y_pred)
        # K.epsilon()는 'divide by zero error' 예방차원에서 작은 수를 더한다
        _f1score = (2 * _recall * _precision) / (_recall + _precision + K.epsilon())

def load_model(yaml_file_name,h5_file_name) :
    yaml_file = open(yaml_file_name, 'r')
    loaded_model_yaml = yaml_file.read()
    print(yaml_file)
    yaml_file.close()
    loaded_model = model_from_yaml(loaded_model_yaml)
    # load weights into new AI_model
    loaded_model.load_weights(h5_file_name)
    loaded_model.compile(loss='sparse_categorical_crossentropy',optimizer='adam',metrics=[f1score])
    return loaded_model


def book_API(search):
    book_list=[]
    for text in search:
        client_id = "qtW2OiOAlSkWxvXskK5V"
        client_secret = "nG5MjeQ1NM"
        encText = urllib.parse.quote(text)
        url = "https://openapi.naver.com/v1/search/book?query=" + encText + "&display=3&sort=count"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            text_data = response_body.decode('utf-8')
            books = json.loads(text_data)
            book_list.extend(books["items"])
        else:
            print("Error Code:" + rescode)
    img_list = []
    title_list = []
    link_list = []
    for i in range(len(book_list)): img_list.append(book_list[i]["image"])
    for i in range(len(book_list)): title_list.append(Markup(str(book_list[i]["title"])))
    for i in range(len(book_list)): link_list.append(Markup(str(book_list[i]["link"])))
    return img_list,title_list,link_list

def developerType_Info(devleloperType,have = "Language"):
    if devleloperType == "Web developer":
        search = ["자바스크립트", "SQL웹", "AWS", "AngularJS"]
        img = "static/img/developerType/Web_developer.png"
        have_info = ["JavaScript", "SQL", "C#", "Java", "PHP",
                     "MySQL", "SQL Server", "PostgreSQL", "MongoDB", "SQLite",
                     "AngularJS", "Node.js", ".NET Core", "React", "Cordova",
                     "AWS", "Linux Desktop", "Android", "Mac OS", "WordPress"]
        graph_path = ["static/img/developerType/Web_HaveWorkedLanguage.png",
                      "static/img/developerType/Web_HaveWorkedDatabase.png",
                      "static/img/developerType/Web_HaveWorkedFramework.png",
                      "static/img/developerType/Web_HaveWorkedPlatform.png"]
        map = ["JavaScript", "SQL", "C샵", "Java", "PHP",
                     "MySQL", "SQLServer", "PostgreSQL", "MongoDB", "SQLite",
                     "AngularJS", "Nodejs", "NETCore", "React", "Cordova",
                     "AWS", "LinuxDesktop", "Android", "MacOS", "WordPress"]
        youtube = "https://www.youtube.com/embed/rhJJlCrjqDo"
        info = ["""● Web developer는 HTTP 프로토콜을 커뮤니케이션 매체로 사용하는 웹 페이지, 웹 사이트 등 WWW 기반 
        소프트웨어 개발자 또는 소프트웨어 엔지니어를 말한다. 대다수의 웹개발자들은 웹 디자인, 정보설계, 사용자 인터페이스 설계, 프로젝트 관리,
         웹 서버 및 데이터베이스 관리, 웹페이지 코딩 및 프로그래밍 관련 기술을 가지고 있다.""",
        "● 직업만족도 : 70.2점","● 재택근무비율 :	70.12%"]
    elif devleloperType == "Mobile developer":
        search = ["자바스크립트 모바일", "MySQL 모바일", "Node.js 모바일", "AngularJS 모바일"]
        img = "static/img/developerType/Mobile_developer.PNG"
        have_info = ["JavaScript", "Java", "SQL", "C#", "PHP",
                     "MySQL", "SQLite", "SQL Server", "PostgreSQL", "MongoDB",
                     "Node.js", "AngularJS", ".NET Core", "Cordova", "Firebase",
                     "Android", "iOS", "AWS", "Mac OS", "Linux Desktop"]
        graph_path = ["static/img/developerType/Mobile_HaveWorkedLanguage.png",
                      "static/img/developerType/Mobile_HaveWorkedDatabase.png",
                      "static/img/developerType/Mobile_HaveWorkedFramework.png",
                      "static/img/developerType/Mobile_HaveWorkedPlatform.png"]
        map = ["JavaScript", "Java", "SQL", "C샵", "PHP",
                     "MySQL", "SQLite", "SQLServer", "PostgreSQL", "MongoDB",
                     "Nodejs", "AngularJS", "NETCore", "Cordova", "Firebase",
                     "Android", "iOS", "AWS", "MacOS", "LinuxDesktop"]
        youtube = "https://www.youtube.com/embed/fB9ylcWBPRs"
        info = ["""● Mobile developer는 모바일기기에서 사용되는 프로그램, 고객의 요구에 적합한 어플리케이션 등을 개발하고 유지·관리·보수한다. 
        달력이나 일정관리, 시계, 카메라 등의 기본 유틸리티뿐 아니라, 지도, 검색, 교통, 커뮤니티, 은행, 교육, 게임, 영화 등 온라인으로 
        볼 수 있는 모든 것들을 앱으로 구현시키는 역할을 한다. 모바일콘텐츠를 개발하려면 먼저 기술력도 있어야 하지만 사람들이 궁금해 하는 
        상황을 정확하게 ""","● 직업만족도 : 71.1점","● 재택근무비율 : 72.85%"]
    elif devleloperType == "Desktop applications developer":
        search = ["SQL Server", ".NET Core", "MySQL", "Linux"]
        img = "static/img/developerType/Desktop_applications_developer.png"
        have_info = ["SQL", "JavaScript", "C#", "Java", "C++",
                     "SQL Server", "MySQL", "SQLite", "PostgreSQL", "Oracle",
                     ".NET Core", "AngularJS", "Node.js", "Xamarin", "React",
                     "Linux Desktop", "Android", "AWS", "Mac OS", "iOS"]
        graph_path = ["static/img/developerType/Desktop_HaveWorkedLanguage.png",
                      "static/img/developerType/Desktop_HaveWorkedDatabase.png",
                      "static/img/developerType/Desktop_HaveWorkedFramework.png",
                      "static/img/developerType/Desktop_HaveWorkedPlatform.png"]
        map =["SQL", "JavaScript", "C샵", "Java", "C쁠쁠",
                     "SQLServer", "MySQL", "SQLite", "PostgreSQL", "Oracle",
                     "NETCore", "AngularJS", "Nodejs", "Xamarin", "React",
                     "LinuxDesktop", "Android", "AWS", "MacOS", "iOS"]
        youtube = "https://www.youtube.com/embed/qZAkIpkPbmc"
        info = ["""● Desktop applications developer는 -	desktop 개발자는 응용 소프트웨어 개발자라고도 하며 소프트웨어를 개발·완성시키기 
        위한 전체적인 개발 계획과 자원 조달 계획을 편성한다. 응용시스템에 대한 정보보호의 방법과 계획을 설정하고 소프트웨어의 세부적인 기능 및 
        사양에 관한 상세 설계를 한다. 해당 컴퓨터시스템에 개발된 프로그램을 설치하고 기능 및 성능을 종합적으로 평가·분석하고 패키지성의 개발 소프트웨어에 
        대해서는 체계적인 버전관리를 한다. 또, 테스트를 통해 버그를 수정하는 역할을 한다. ""","● 직업만족도 : 68.9점","● 재택근무비율 : 76.49%"]
    elif devleloperType == "Database administrator":
        search = ["SQL Server", "Node.js", "MySQL", "AWS"]
        img = "static/img/developerType/Database_administrator.png"
        have_info = ["SQL", "JavaScript", "C#", "PHP", "Java",
                     "MySQL", "SQL Server", "PostgreSQL", "SQLite", "MongoDB",
                     "Node.js", "AngularJS", ".NET Core", "React", "Cordova",
                     "AWS", "Linux Desktop", "Android", "WordPress", "Mac OS"]
        graph_path = ["static/img/developerType/Database_HaveWorkedLanguage.png",
                      "static/img/developerType/Database_HaveWorkedDatabase.png",
                      "static/img/developerType/Database_HaveWorkedFramework.png",
                      "static/img/developerType/Database_HaveWorkedPlatform.png"]
        map = ["SQL", "JavaScript", "C샵", "PHP", "Java",
                     "MySQL", "SQLServer", "PostgreSQL", "SQLite", "MongoDB",
                     "Nodejs", "AngularJS", "NETCore", "React", "Cordova",
                     "AWS", "LinuxDesktop", "Android", "WordPress", "MacOS"]
        youtube = "https://www.youtube.com/embed/oNuIAA5LvUQ"
        info = ["""● Database administrator는 데이터베이스를 설계하고, 최적화를 위한 관리 업무를 수행한다. 일반적으로 전문대학 및 대학교에서 컴퓨터공학, 
        전산학, 수학 등을 전공하고 진출한다. 각종 데이터베이스관리시스템을 비롯해 데이터베이스의 운영과 관련한 하드웨어 및 소프트웨어에 대한 지식이 필요하다.""",
                "● 직업만족도 : 68.9점","● 재택근무비율 : 	77.59"]
    elif devleloperType == "Data scientist":
        search = ["SQL Server", "Node.js", "MySQL", "Linux"]
        img = "static/img/developerType/Data_scientist.jpg"
        have_info = ["SQL", "JavaScript", "Python", "Java", "C#",
                     "MySQL", "SQL Server", "PostgreSQL", "MongoDB", "SQLite",
                     "Node.js", "AngularJS", ".NET Core", "Hadoop", "Spark",
                     "Linux Desktop", "AWS", "Android", "Mac OS", "Raspberry Pi"]
        graph_path = ["static/img/developerType/Data_HaveWorkedLanguage.png",
                      "static/img/developerType/Data_HaveWorkedDatabase.png",
                      "static/img/developerType/Data_HaveWorkedFramework.png",
                      "static/img/developerType/Data_HaveWorkedPlatform.png"]
        map = ["SQL", "JavaScript", "Python", "Java", "C샵",
                     "MySQL", "SQLServer", "PostgreSQL", "MongoDB", "SQLite",
                     "Nodejs", "AngularJS", "NETCore", "Hadoop", "Spark",
                     "LinuxDesktop", "AWS", "Android", "MacOS", "RaspberryPi" ]
        youtube = "https://www.youtube.com/embed/-tmypCjhfkE"
        info = ["""● Data scientist는 복잡한 비즈니스 문제를 모델링하고 인사이트를 도추라며 통계학, 알고리즘, 데이터 마이닝, 
        시각화를 통해 그 속에서 기회를 찾아내는 사람이다. 이런 고급분석기술에 더해, 용량이 크고 다양한 유형의 dataset 을 다루는데 능숙하고, 
        특정한 목적 혹은 컴퓨팅 환경의 데이터 베이스 아키텍처를 수립할 수 있으며 분석결과를 이해 관계자들과 커뮤니케이션 할 수 있어야한다. ""","● 직업만족도 : 72.2점","● 재택근무비율 : 	76.05%"]
    else:
        pass
    return search,img,info, have_info, graph_path,youtube,map