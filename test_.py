import unittest
from flask import Flask, Request, request

import utils, models
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
        self.model = models.PayrollReport(DB_NAME)

    def tearDown(self):
        self.model.close_conn()
        os.remove(DB_NAME +'.db')

    def test_index(self):
        res = app.test_client().get('/')
        assert res.status_code == 200
        assert res.data == b'Hello, World!'

    def test_read_file(self):
        filename = 'time-report-42.csv'
        with open(filename,'rb') as csvFile:
            data = {'file': (filename, csvFile,'text/csv')}
            res = utils.read_file(csvFile)
        csvFile.close()
        # app.logger.info(res[0])
        self.assertEqual(res[0], 200)


    def test_parse_report_id(self):
        filename = 'time-report-42.csv'
        res,msg,id = utils.get_report_id(filename)
        self.assertEqual(res, 200)
        self.assertEqual(id, 42)


    def test_existing_report_id(self):
        filename = 'time-report-42.csv'
        with open(filename,'rb') as csvFile:
            data = {'file': (filename, csvFile,'text/csv')}
            _,_,data_ = utils.read_file(csvFile)
        csvFile.close()
        status, msg, df = utils.parse_employee_logs(data_, 42)
        self.assertEqual(status, 200)
        self.assertEqual(msg, "successfully parsed employee data")
        status, msg = self.model.insert_csv(df, 42)
        self.assertEqual(status, 200)
        self.assertEqual(msg, "Updated table")

        status, msg = self.model.insert_csv(df, 42)
        self.assertEqual(status, 400)
        self.assertEqual(msg, "report id already exists")


    def test_get_payroll_report_42(self):
        filename = 'time-report-42.csv'
        with open(filename,'rb') as csvFile:
            data = {'file': (filename, csvFile,'text/csv')}
            _,_,data_ = utils.read_file(csvFile)
        csvFile.close()

        status, msg, df = utils.parse_employee_logs(data_, 42)
        status, msg = self.model.insert_csv(df, 42)

        rows = self.model.get_logs()
        status, payrollReport = utils.make_payroll_report(rows)
        # app.logger.info(json.dumps(payrollReport, indent = 4))
        self.assertEqual(status, 200)

    def test_get_payroll_report_01(self):
        filename = 'time-report-01.csv'
        with open(filename,'rb') as csvFile:
            data = {'file': (filename, csvFile,'text/csv')}
            _,_,data_ = utils.read_file(csvFile)
        csvFile.close()
        _,_,id = utils.get_report_id(filename)
        _, _, df = utils.parse_employee_logs(data_, id)
        _, _ = self.model.insert_csv(df, id)


        rows = self.model.get_logs()
        status, payrollReport = utils.make_payroll_report(rows)
        # app.logger.info(json.dumps(payrollReport, indent = 4))

        self.assertEqual(status, 200)
        check_amount = payrollReport["payrollReport"]['employeeReports'][0]['amountPaid']
        self.assertEqual(check_amount, "$300.00")

    def test_front_end_file_upload(self):
        # data = {'file': ('time-report-42.csv', open('time-report-42.csv', 'rb'),'text/csv')}
        filename = 'time-report-42.csv'
        with open('time-report-42.csv','rb') as csvFile:
            data = {'file': ('time-report-42.csv', csvFile,'text/csv')}
            res = self.app.post('/upload_payroll',data=data)
        csvFile.close()
        self.assertEqual(res.status_code, 400)


    def test_front_end_get_payroll_report(self):
        res = self.app.get('/payroll_report')
        # app.logger.info(json.dumps(report.data, indent = 4))
        # app.logger.info(report.data)
        self.assertEqual(res.status_code, 200)

        is_json = False
        if(json.loads(res.data)):
            is_json = True
            # app.logger.info(json.dumps(json.loads(res.data), indent=4))
        self.assertEqual(is_json, True)


if __name__ == "__main__":
    unittest.main()
