from flask import Flask,g,make_response,Response,request,render_template,session
from pymongo import MongoClient
import numpy as np

app =Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8zdkjsfhqw]/'
# try :
#     client = MongoClient('mongodb://localhost:27017')
#     if "member" not in client.list_database_names():
#         db = client['member']
#         collect = db['Account']
#         data = {'id': 'ydy1412', 'password': '920910'}
#         collect.insert_one(data)
#         client.close()
#     else:
#         client.close()
# except :
#     print("db problem happend")

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
        return render_template('re_page.html')
    else :
        return "no id"

@app.route('/final_page', methods=['GET', 'POST'])
def test1():
    def transform_numpy_array() :
        if request.method == 'POST':
            ProblemSolving = request.form["ProblemSolving"]  #

            BuildingThings = request.form["BuildingThings"]  #
            LearningNewTech = request.form["LearningNewTech"]
            BoringDetails = request.form["BoringDetails"]
            JobSecurity = request.form["JobSecurity"]
            DiversityImportant = request.form["DiversityImportant"]
            AnnoyingUI = request.form["AnnoyingUI"]
            FriendsDevelopers = request.form["FriendsDevelopers"]
            RightWrongWay = request.form["RightWrongWay"]
            UnderstandComputers = request.form["UnderstandComputers"]
            SeriousWork = request.form["SeriousWork"]
            InvestTimeTools = request.form["InvestTimeTools"]
            WorkPayCare = request.form["WorkPayCare"]
            ChallengeMyself = request.form["ChallengeMyself"]
            CompetePeers = request.form["CompetePeers"]
            ChangeWorld = request.form["ChangeWorld"]
            AssessJobRole = request.form["AssessJobRole"]
            AssessJobRemote = request.form["AssessJobRemote"]
            AssessJobProduct = request.form["AssessJobProduct"]
            AssessJobProfDevel = request.form["AssessJobProfDevel"]
            ImportantHiringEducation = request.form["ImportantHiringEducation"]
            ImportantHiringCommunication = request.form["ImportantHiringCommunication"]
            EducationTypes = request.form["EducationTypes"]
            ImportantBenefits = request.form["ImportantBenefits"]
            FormalEducation = request.form["FormalEducation"]
            MajorUndergrad = request.form["MajorUndergrad"]
            answer_list = [ProblemSolving, BuildingThings, LearningNewTech,
                           BoringDetails, JobSecurity, DiversityImportant,
                           AnnoyingUI, FriendsDevelopers, RightWrongWay,
                           UnderstandComputers, SeriousWork, InvestTimeTools,
                           WorkPayCare, ChallengeMyself, CompetePeers, ChangeWorld,
                           AssessJobRole, AssessJobRemote, AssessJobProduct, AssessJobProfDevel,
                           ImportantHiringEducation, ImportantHiringCommunication, FormalEducation,
                           MajorUndergrad, EducationTypes, ImportantBenefits]
            Input_data = np.array(answer_list)
            return Response(Input_data.shape)
    return render_template("Q1.html")

if __name__ == "__main__" :
    app.debug = True
    app.run(host = "0.0.0.0")
