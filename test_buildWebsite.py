import buildWebsite
import unittest
from database import commentData


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        buildWebsite.app.config['Testing'] = True
        self.app = buildWebsite.app.test_client()

    def test_newComment(self):

        self.app.post('/Assignment3.0/Version/7449/File/buildWebsite.py', data=dict(
            userName='dz3264',
            commentContext='Test new parent comment'
        ), follow_redirects=True)

        lastEnrty = commentData.read_test()
        print(lastEnrty)
        assert 'dz3264' == lastEnrty[1]
        assert 'Test new parent comment' == lastEnrty[2]
        assert None == lastEnrty[4] and None == lastEnrty[5] and None == lastEnrty[6]
        assert 'buildWebsite.py' == lastEnrty[7]

    def test_childComment(self):
        self.app.post('/Assignment3.0/Version/7449/File/buildWebsite.py', data=dict(
            bsubmit=10,
            rpName='hzhan107',
            replyParent = 'Test new child comment'
        ), follow_redirects=True)

        lastEnrty = commentData.read_test()
        print(lastEnrty)
        #assert 'hzhan107' == lastEnrty[1]
        #assert 'Test new child comment' == lastEnrty[2]
        #assert 18 == lastEnrty[4]
        #assert None == lastEnrty[5] and None == lastEnrty[6]
        #assert 'buildWebsite.py' == lastEnrty[7]


    def test_childReply(self):
        self.app.post('/Assignment3.0/Version/7449/File/buildWebsite.py', data=dict(
            bsubmit= '18.20' ,
            rcName='child',
            replyChild = 'Test child reply comment'
        ), follow_redirects=True)

        lastEnrty = commentData.read_test()
        print(lastEnrty)
        #assert 'child' == lastEnrty[1]
        #assert 'Test child reply comment' == lastEnrty[2]
        #assert 18 == lastEnrty[4]
        #assert 20 == lastEnrty[5]
        #assert 'hzhan107' == lastEnrty[6]
        #assert 'buildWebsite.py' == lastEnrty[7]



if __name__ == '__main__':
    unittest.main()
# Source http://stackoverflow.com/questions/32290830/how-to-unit-test-a-form-submission-when-multiple-forms-on-a-route