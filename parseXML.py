import xml.etree.ElementTree as et

class parseSVNclass:

    def openFile(self, filename):
        file = open(filename,'r')
        data = file.read()
        return data



    # go throught all element on the subversion and parse them into dictionary
    def parseProj(self,logfile):
        tree = et.parse(logfile)
        root = tree.getroot()

        projects = []

        for logs in root:

            project = {
                "Title": None,
                "Version": logs.attrib['revision'],
                "LogsInfo":[],
                "Files":[] # filelist in this project
            }
            logsInfo = {}
            pathList = []
            for child in logs:
                if(child.tag == "paths"):

                    # find all file path in paths
                    filePath = child.findall("path")
                    for path in filePath:

                        paresdPath = path.text.split("/")
                        #print(paresdPath)
                        if(path.attrib["kind"] == "file"
                           and ("html" in paresdPath[len(paresdPath)-1] or "java" in paresdPath[-1] or "cpp" in paresdPath[-1] or "py" in paresdPath[-1])
                           and "init" not in paresdPath[-1] and "idea" not in paresdPath[-2] and 'description' not in paresdPath[-1]):
                            #print(paresdPath)
                            pathList.append(path.text)

                    # parse the name of the project from path

                        if (len(paresdPath)>2
                            and ("html" in paresdPath[len(paresdPath)-1] or "java" in paresdPath[len(paresdPath)-1] or "cpp" in paresdPath[len(paresdPath)-1] or "py" in paresdPath[len(paresdPath)-1])):
                            project["Title"] = paresdPath[2]

                    logsInfo["paths"] = pathList

                else:
                    logsInfo[child.tag] = child.text

            project["LogsInfo"] = logsInfo
            projects.append(project)

        projectList = {}

        for proj in projects:
            # Check if there already contain the same project but different version
            if proj["Title"] in list(projectList.keys()):
                projectList[proj["Title"]]["UpdateVersions"].append(proj)

            else:

                projectList[proj["Title"]] = {
                    "Name": proj["Title"],
                    "UpdateVersions":[]
                }

                projectList[proj["Title"]]["UpdateVersions"].append(proj)


        return projectList


    def parseFile(self,logfile,listfile):

        projectList = self.parseProj(logfile);
        #print(projectList)

        tree = et.parse(listfile)
        root = tree.getroot()

        # get the list in root lists
        list = root.findall("list")
        list = list[0]

        # go throught entery/files in list
        for entry in list:

            if (entry.attrib["kind"] == "file"):
                file = {}
                for infos in entry:

                    if (infos.tag == "commit"):
                        file[infos.tag] = infos.attrib
                        for i in infos:
                            file[i.tag] = i.text
                    else:
                        file[infos.tag] = infos.text

                parseName = file["name"].split(".")
                file["Type"] = parseName[len(parseName)-1]
                # check if this is a test file
                # Maybe changes types into: code, test, documentation, and so on ?
                if ((file["Type"] == "py" or file["Type"] == "java" or file["Type"] == "html" ) and "Test" in file["name"]):
                    file["Type"] = "Test."+ file["Type"]


                assignment = file["name"].split("/")[0]
                if "Assignment" in assignment:
                    for p in projectList[assignment]["UpdateVersions"]:
                        if(p["Version"] == file["commit"]["revision"]
                           and ("java" in file["name"] or "cpp" in file["name"] or "py" in file["name"] or file["Type"] == "html" )
                           and "init" not in file["name"] and 'description' not in file["name"]):
                            p["Files"].append(file)
                            #print(file["name"])
                #print(file["commit"]["revision"])

        return projectList

    #def parseCode(self):

#testProjects = parseSVNclass().parseProj('svn_log_test.xml')

#parseSVNclass().parseFile("svn_log.xml", "svn_list.xml")
#projProtfolio = parseSVNclass().parseFile()

#print(projProtfolio)


# Source Cite: https://docs.python.org/2/library/xml.etree.elementtree.html