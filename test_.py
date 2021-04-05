import unittest
from flask import Flask, Request, request
# import src
from copy import deepcopy

import pandas as pd
import helpers
import pytest
import requests
import json

from app import app
# from base import BaseestCase

# app = Flask(__name__)

# url = 'http://127.0.0.1:5000' # The root url of the flask app
#
# app.testing = True
# app.config['TESTING'] = True  # to get full tracebacks in our tests

#     self.app = app.test_client()
class TestUploadFileEndpoint(unittest.TestCase):
    def setUp(self):
        # self.backup_items = deepcopy(app.items)  # no references!
        self.app = app.test_client()
        self.app.testing = True
    #
    # def test_base_route(self):
    #     # client = self.test_client()
    #     response = self.app.get('/')
    #     app.logger.info(response)
    def test_hello(self):
        response = app.test_client().get('/')
        app.logger.info("test hello")
        assert response.status_code == 200
        assert response.data == b'Hello, World!'

    # def test_file_upload(self):
    #     # data = {'file': ('time-report-42.csv', open('time-report-42.csv', 'rb'),'text/csv')}
    #     with open('time-report-42.csv','rb') as csvFile:
    #         # cvsReader = csvFile.reader(csvFile,delimiter = ',')
    #         data = {'file': ('time-report-42.csv', csvFile,'text/csv')}
    #         res = self.app.post('/upload_payroll',data=data)
    #
    #     csvFile.close()
    #     app.logger.info(res.data)
    #     self.assertEqual(res.status_code, 200)

    def test_read_file(self):
        filename = 'time-report-42.csv'
        with open(filename,'rb') as csvFile:
            data = {'file': (filename, csvFile,'text/csv')}
            res = helpers.read_file(csvFile)
        csvFile.close()
        # app.logger.info(res[0])
        self.assertEqual(res[0], 200)


    def test_parse_report_id(self):
        filename = 'time-report-42.csv'
        res,msg,data = helpers.get_report_id(filename)
        self.assertEqual(res, 200)
        self.assertEqual(data, 42)

    # def test_to_database_existing_report_id(self):
    #     filename = 'time-report-42'
    #     with open('time-report-42.csv','rb') as csvFile:
    #         data = {'file': ('time-report-42.csv', csvFile,'text/csv')}
    #         res = helpers.to_database(csvFile)
    #     csvFile.close()
    #     # app.logger.info(res[0])
    #     self.assertEqual(res[0], 200)

    def test_existing_report_id(self):
        res = helpers.check_report_id_exsists('42')
        # app.logger.info(res)
        self.assertEqual(True, res)

class TestGetPayrollReportEndpoint(unittest.TestCase):
    def setUp(self):
        # self.backup_items = deepcopy(app.items)  # no references!
        self.app = app.test_client()
        self.app.testing = True
    # case 1
    def test_simple_payroll_report(self):
        res = helpers.make_payroll_report()
        self.assertEqual(200, res)



if __name__ == "__main__":
    unittest.main()
