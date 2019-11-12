from flask import Flask,g,make_response,Response,request,render_template
from flask import session, render_template, Markup
import urllib.request
import json
from API import book_API, developerType_Info

app =Flask(__name__)

app.debug = True

@app.route("/")
def helloworld2():
    return render_template('main_page.html')

@app.route("/sur")
def sur():
    return render_template('Q1.html')

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

# @app.route("/member_checked",methods = ['POST'])
# def member_checked():
#     id = request.form['id']
#     password = request.form['password']
#     client = MongoClient('mongodb://localhost:27017')
#     db = client['member']
#     collect = db['Account']
#     login_data = {"id": str(id),"password" : str(password)}
#     Id_existence = collect.find_one(login_data)
#     client.close()
#     if Id_existence is not None :
#         return render_template('re_page.html')
#     else :
#         return "no id"

@app.route("/final_page",methods = ['POST'])
def final_page():
    if request.method == 'POST':
        try :
            ProblemSolving = request.form["ProblemSolving"]
            BuildingThings = request.form["BuildingThings"]
            LearningNewTech =request.form["LearningNewTech"]
            BoringDetails = request.form["BoringDetails"]
            JobSecurity = request.form["JobSecurity"]
            DiversityImportant=request.form["DiversityImportant"]
            AnnoyingUI=request.form["AnnoyingUI"]
            FriendsDevelopers=request.form["FriendsDevelopers"]
            RightWrongWay=request.form["RightWrongWay"]
            UnderstandComputers=request.form["UnderstandComputers"]
            SeriousWork=request.form["SeriousWork"]
            InvestTimeTools=request.form["InvestTimeTools"]
            WorkPayCare=request.form["WorkPayCare"]
            ChallengeMyself=request.form["ChallengeMyself"]
            CompetePeers=request.form["CompetePeers"]
            ChangeWorld=request.form["ChangeWorld"]
            AssessJobRole=request.form["AssessJobRole"]
            AssessJobRemote=request.form["AssessJobRemote"]
            AssessJobProduct=request.form["AssessJobProduct"]
            AssessJobProfDevel=request.form["AssessJobProfDevel"]
            ImportantHiringEducation=request.form["ImportantHiringEducation"]
            ImportantHiringCommunication=request.form["ImportantHiringCommunication"]
            EducationTypes=request.form["EducationTypes"]
            ImportantBenefits=request.form["ImportantBenefits"]
            FormalEducation=request.form["FormalEducation"]
            MajorUndergrad=request.form["MajorUndergrad"]
            return "yes"
        except :
            return ""
    return render_template("Login.html")

@app.route('/result', methods=['GET', 'POST'])
def result():

    # devleloperType = "Web developer"
    devleloperType = "Mobile developer"

    #devleloperType = "Desktop applications developer"

    search,img,info, have_info, graph_path, youtube,map = developerType_Info(devleloperType)
    img_list,title_list,link_list = book_API(search)

    return render_template("result_transform.html",
                           img = img,
                           info=info,
                           devleloperType= devleloperType,
                           graph_path = graph_path,
                           have_info=have_info,
                           page1_img=img_list[:6],
                           page1_title=title_list[:6],
                           page1_link=link_list[:6],
                           page2_img=img_list[6:],
                           page2_title=title_list[6:],
                           page2_link=link_list[6:],
                           youtube = youtube,
                           map= map)


if __name__ == '__main__':
    app.run(debug=True,threaded=True,host='0.0.0.0')