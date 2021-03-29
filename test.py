import unittest
from flask import Flask, Request, request
# import src
from io import StringIO
import pandas as pd
import helpers

        # app.request_class = MyRequest
# def setUp(self):
#     app = create_app('flask_test.cfg')
app = Flask(__name__)

app.testing = True
#     self.app = app.test_client()
app.debug = True
class TestCSVEndpoint(unittest.TestCase):
    # def setUp(self):

    # def test_csv_specification(self):
    #     self.data = "time-report-42.csv"
    #     result = self.test_client.post('upload_file', {'file':self.data})
    #     self.assertEqual()

    # def test_1(self):
    #     client = app.test_client()
    #     response = client.get('/')
    #     assert response.status_code == 200

    # def test_1(self):
    #     self.data = "time-report-42.csv"
    #     response = self.client.test_client.post('/upload_payroll', data = {
    #         'file':(StringIO('my file contents'), self.data)
    #     })
    #     self.assertEqual(response.status_code, 200)
    def test_read_file(self):
        client = app.test_client() # you will need your flask app to create the test_client
        # data = {
        #     'file': (pd.read_csv('time-report-42.csv'))
        # }
        app.logger.info("Hello world - app.logger.info")
        payroll_data = helpers.read_file("time-report-42.csv")
        app.logger.info(payroll_data)
    # def test_file_upload(self):
    #     client = app.test_client() # you will need your flask app to create the test_client
    #     data = {
    #         'file': (pd.read_csv('time-report-42.csv'))
    #     }
    #     # note in that in the previous line you can use 'file' or whatever you want.
    #     # flask client checks for the tuple (<FileObject>, <String>)
    #     res = client.post('/upload_payroll', data=data)
    #     print(res.status_code, file=sys.stderr)
    #     assert res.status_code == 200


        # result = self.read_csv()

    # def test_timekeeping_in_database(self):
    #
    #
    # def test_same_report_id(self):


if __name__ == "__main__":
    unittest.main()
