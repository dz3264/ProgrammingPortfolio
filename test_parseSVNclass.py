from unittest import TestCase
from parseXML import parseSVNclass

class TestParseSVNclass(TestCase):
    def test_parseProj(self):
        s = TestParseSVNclass()
        self.assertRaises(Exception)

        testProjects = parseSVNclass().parseProj('svn_log_test.xml')


        self.assertEqual("Assignment2.1", testProjects["Assignment2.1"]["Name"])
        self.assertEqual("Assignment2.0", testProjects["Assignment2.0"]["Name"])

        self.assertEqual("hzhan107", testProjects["Assignment2.1"]["UpdateVersions"][0]["LogsInfo"]["author"])

        self.assertEqual("6538", testProjects["Assignment2.1"]["UpdateVersions"][0]["Version"])
        self.assertEqual("4436", testProjects["Assignment2.1"]["UpdateVersions"][1]["Version"])

        self.assertEqual(True, "/hzhan107/Assignment2.1/WebScrap/Graph/DataAnalysis.py" in
                         testProjects["Assignment2.1"]["UpdateVersions"][0]["LogsInfo"]["paths"])
        self.assertEqual(False, "/hzhan107/Assignment2.1/WebScrap/Graph/DataAnalysis.py" in
                         testProjects["Assignment2.1"]["UpdateVersions"][1]["LogsInfo"]["paths"])


        self.assertEqual(False, "/hzhan107/Assignment2.0/.idea/Assignment 2.0.iml" in
                         testProjects["Assignment2.0"]["UpdateVersions"][0]["LogsInfo"]["paths"])

        self.assertEqual(True, "/hzhan107/Assignment2.0/WebScrap/QueriesFunc.py" in
                         testProjects["Assignment2.0"]["UpdateVersions"][0]["LogsInfo"]["paths"])

    def test_parseFile(self):
        s = TestParseSVNclass()
        self.assertRaises(Exception)

        testProtfolio = parseSVNclass().parseFile('svn_log_test.xml',"svn_list_test.xml")

        self.assertEqual("Assignment2.1", testProtfolio["Assignment2.1"]["Name"])
        self.assertEqual("Assignment2.0", testProtfolio["Assignment2.0"]["Name"])


        self.assertEqual("Assignment2.0/WebScrap/QueriesFunc.py", testProtfolio["Assignment2.0"]["UpdateVersions"][0]["Files"][0]["name"])
        self.assertEqual("5469",testProtfolio["Assignment2.0"]["UpdateVersions"][0]["Files"][0]["size"])

        self.assertEqual(False, "Assignment2.0/.idea/Assignment 2.0.iml" in
                         testProtfolio["Assignment2.0"]["UpdateVersions"][0]["Files"])

        self.assertEqual("Assignment2.1/WebScrap/Graph/DataAnalysis.py",
                         testProtfolio["Assignment2.1"]["UpdateVersions"][0]["Files"][0]["name"])
        self.assertEqual("3849",testProtfolio["Assignment2.1"]["UpdateVersions"][0]["Files"][0]["size"])

        self.assertEqual("Assignment2.1/WebScrap/Graph/DataGraphLib.py",
                         testProtfolio["Assignment2.1"]["UpdateVersions"][0]["Files"][1]["name"])
        self.assertEqual("6161", testProtfolio["Assignment2.1"]["UpdateVersions"][0]["Files"][1]["size"])

        self.assertEqual("Assignment2.1/WebScrap/Graph/GraphLibrary.py",
                         testProtfolio["Assignment2.1"]["UpdateVersions"][0]["Files"][2]["name"])
        self.assertEqual("5732", testProtfolio["Assignment2.1"]["UpdateVersions"][0]["Files"][2]["size"])



        print(testProtfolio)
