from parseXML import parseSVNclass
from flask import Flask, render_template, request
from database import commentData


codeProtfolio = parseSVNclass().parseFile("svn_log.xml","svn_list.xml")
commentData.create_table()

app = Flask(__name__)

#home page with every project and some infos
@app.route("/")
def protfolio():

    # Get Project Names
    projectsName = []
    for proj in list(codeProtfolio.keys()):
        if proj != None and "Assignment" in proj:
            projectsName.append(proj)

    # Project Bref Infos
    return render_template("portfolioTemplate.html",projectsName = sorted(projectsName), projectList = codeProtfolio)


@app.route("/<Assignment>")
def projects(Assignment):
    projectVersions = []
    for proj in codeProtfolio[Assignment]["UpdateVersions"]:
        projectVersions.append(proj["Version"])

    #print(projectVersions)
    return render_template("versionTemplate.html",Assignment = Assignment, projectVersions = projectVersions, project = codeProtfolio[Assignment])


@app.route("/<Assignment>/Version/<VersionNum>")
def versions(Assignment,VersionNum):
    fileName = []
    for ver in codeProtfolio[Assignment]["UpdateVersions"]:
        if(VersionNum == ver["Version"]):
            project = ver
            for file in ver["Files"]:
                fileName.append(file["name"].split("/")[-1])

    return render_template("projectTemplate.html",assignment = Assignment,VersionNum = VersionNum, project = project,fileName=fileName)



@app.route("/<Assignment>/Version/<VersionNum>/File/<FileName>", methods = ['GET','POST'])
def files(Assignment,VersionNum,FileName):
    # get comment NO parent
    backlink = "/" + Assignment + "/Version/" + VersionNum + "/File/" + FileName
    fliterWord = ['fuck','shit','asshole','stupid','hell']
    flag = False
    if request.method == 'POST':
        # parent comment
        if 'commentContext' in request.form :
            uName = request.form['userName']
            cContext = request.form['commentContext']

            if(cContext != ''):
                for w in fliterWord:
                    if w in cContext.lower() or w in uName.lower():
                        flag = True

                if (flag == False):
                    if (uName == ''):
                        uName = "Anonymous"
                    commentData.dynamic_data_entry(commentData.data_size(),uName,cContext, None, None,FileName)
                else:
                    return render_template("filterPage.html", backlink = backlink)


        # children comment
        if 'replyParent' in request.form :

            pid = request.form['bsubmit']
            rpN = request.form['rpName']
            replyP = request.form['replyParent']
            if (replyP != ''):
                for w in fliterWord:
                    if w in replyP.lower() or w in rpN.lower():
                        flag = True
                if (flag == False):
                    if (rpN == ''):
                        rpN = "Anonymous"
                    commentData.dynamic_data_entry(commentData.data_size(), rpN, replyP, pid, None, FileName)
                else:
                    return render_template("filterPage.html", backlink=backlink)

        if 'replyChild' in request.form:
            pid = None
            cid = None
            ParentReply = request.form['bsubmit']
            ParentReply = (str(ParentReply)).split('.')
            pid = int(ParentReply[0])
            if(len(ParentReply) > 1):
                cid = int(ParentReply[1])
            rcN = request.form['rcName']
            replyC = request.form['replyChild']
            if (replyC != ''):
                for w in fliterWord:
                    if w in replyC.lower() or w in rcN.lower():
                        flag = True

                if (flag == False):
                    if (rcN == ''):
                        rcN = "Anonymous"
                    commentData.dynamic_data_entry(commentData.data_size(), rcN, replyC, pid, cid,  FileName)
                else:
                    return render_template("filterPage.html", backlink=backlink)

    # Get All comment of current File
    commentList = commentData.read_from_db(FileName)

    parentList = commentData.read_parent(FileName)
    childList = []
    for p in parentList:
        com = {
            'Parent': p[0],
            'Children': commentData.read_child(FileName, p[0])
        }
        childList.append(com)

    # get file's link
    host = "https://subversion.ews.illinois.edu/svn/sp17-cs242/hzhan107/"
    files = []

    #filelink = []

    for ver in codeProtfolio[Assignment]["UpdateVersions"]:
        if(ver["Version"] == VersionNum):
            for file in ver["Files"]:
            # All files
                files.append(file["name"].split("/")[-1])
            # Get the specific file link to the subversion
                if file["name"].split("/")[-1] == FileName:
                    filelink = host + file["name"]
    return render_template("fileTemplate.html",Assignment = Assignment, VersionNum = VersionNum, fileName = files,
                           link = filelink, FileName = FileName, project = codeProtfolio[Assignment],
                           commentList = commentList, parentList = parentList, childList = childList)





if __name__ == "__main__":
    app.run()



# Source Cite: https://www.youtube.com/watch?v=t3yHNZhSXLE