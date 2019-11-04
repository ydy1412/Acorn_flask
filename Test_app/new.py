from flask import Flask,g,make_response,Response,request,render_template
from flask import session, render_template, Markup
app =Flask(__name__)

app.debug = True

@app.route('/', methods=['GET', 'POST'])

def test1():
    if request.method == 'POST':

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
        result = {"ProblemSolving": ProblemSolving, "BuildingThings": BuildingThings,"LearningNewTech":LearningNewTech,"BoringDetails":BoringDetails,
                  "JobSecurity":JobSecurity,"DiversityImportant":DiversityImportant,"AnnoyingUI": AnnoyingUI ,"FriendsDevelopers":FriendsDevelopers,
                  "RightWrongWay":RightWrongWay,"UnderstandComputers":UnderstandComputers,"SeriousWork":SeriousWork,"InvestTimeTools":InvestTimeTools,
                  "WorkPayCare":WorkPayCare,"ChallengeMyself":ChallengeMyself,"CompetePeers":CompetePeers,"ChangeWorld":ChangeWorld,
                  "AssessJobRole":AssessJobRole,"AssessJobRemote":AssessJobRemote,"AssessJobProduct":AssessJobProduct,"AssessJobProfDevel":
                  AssessJobProfDevel,"ImportantHiringEducation":ImportantHiringEducation,"ImportantHiringCommunication":ImportantHiringCommunication,
                  "EducationTypes":EducationTypes,"ImportantBenefits":ImportantBenefits,"FormalEducation":FormalEducation}
        return result

    return render_template("Q1.html")


if __name__ == '__main__':
    app.run(debug=True,threaded=True)