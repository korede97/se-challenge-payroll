import unittest
from flask import Flask, Request, request

import utils, model
import json
import sqlite3 as sqlite3
from app import app
import os
# conn = sqlite3.connect("mock_payroll.db")

# from base import BaseestCase

# app = Flask(__name__)

# url = 'http://127.0.0.1:5000' # The root url of the flask app
#
# app.testing = True
# app.config['TESTING'] = True  # to get full tracebacks in our tests

#     self.app = app.test_client()
DB_NAME = 'mock_payroll'

class TestUploadFileEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.db = model.PayrollReport(DB_NAME)

    def tearDown(self):
        self.db.close_conn()
        os.remove(DB_NAME +'.db')


    def test_index(self):
        response = app.test_client().get('/')
        app.logger.info("test index")
        assert response.status_code == 200
        assert response.data == b'Hello, World!'

    def test_file_upload_42(self):
        # data = {'file': ('time-report-42.csv', open('time-report-42.csv', 'rb'),'text/csv')}
        with open('time-report-42.csv','rb') as csvFile:
            # cvsReader = csvFile.reader(csvFile,delimiter = ',')
            data = {'file': ('time-report-42.csv', csvFile,'text/csv')}
            res = self.app.post('/upload_payroll',data=data)

        csvFile.close()
        app.logger.info(res.data)
        self.assertEqual(res.status_code, 200)

    def test_file_upload_01(self):
        # data = {'file': ('time-report-42.csv', open('time-report-42.csv', 'rb'),'text/csv')}
        with open('time-report-01.csv','rb') as csvFile:
            # cvsReader = csvFile.reader(csvFile,delimiter = ',')
            data = {'file': ('time-report-01.csv', csvFile,'text/csv')}
            res = self.app.post('/upload_payroll',data=data)

        csvFile.close()
        app.logger.info(res.data)
        self.assertEqual(res.status_code, 200)

    # def test_read_file(self):
    #     filename = 'time-report-42.csv'
    #     with open(filename,'rb') as csvFile:
    #         data = {'file': (filename, csvFile,'text/csv')}
    #         res = utils.read_file(csvFile)
    #     csvFile.close()
    #     # app.logger.info(res[0])
    #     self.assertEqual(res[0], 200)


    # def test_parse_report_id(self):
    #     filename = 'time-report-42.csv'
    #     res,msg,id = utils.get_report_id(filename)
    #     self.assertEqual(res, 200)
    #     self.assertEqual(id, 42)
    #
    # def test_existing_report_id(self):
    #     filename = 'time-report-42'
    #     with open('time-report-42.csv','rb') as csvFile:
    #         data = {'file': ('time-report-42.csv', csvFile,'text/csv')}
    #         _,_,data_ = utils.read_file(csvFile)
    #     csvFile.close()
    #     status, msg, df = utils.parse_employee_logs(data_, 42)
    #     status, msg = self.db.insert_csv(df, 42)
    #
    #
    #     # app.logger.info(res[0])
    #     self.assertEqual(status, 400)
    #     self.assertEqual(msg, "report id already exists")



    def test_get_payroll_report(self):
        report = self.app.get('/payroll_report')
        # app.logger.info(json.dumps(report.data, indent = 4))
        # app.logger.info(report.data)
        self.assertEqual(report.status_code, 200)

    # def test_get_payroll_report(self):
    #     rows = self.db.get_records()
    #     report = utils.new_report(rows)
        # app.logger.info(json.dumps(report.data, indent = 4))
        # app.logger.info(report.data)
        # self.assertEqual(report.status_code, 200)



if __name__ == "__main__":
    unittest.main()
