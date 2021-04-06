# import flask
from flask import Flask, request, jsonify, make_response
from werkzeug.utils import secure_filename
import json

import os
import sqlite3 as sql
import pandas as pd
import logging
import utils, model

# logging.basicConfig(level=logging.DEBUG)
model = model.PayrollReport('payroll')

app = Flask(__name__)

# @app.route("/", methods=["GET", "POST"])
# def index():
#     return render_template("upload.html")

@app.route('/')
def index():
    return 'Hello, World!'

# @app.route('/')
# def index():
#     return jsonify({'hello': 'world'})

# Upload a CSV file containing data on the number of hours worked per day per employee
@app.route("/upload_payroll", methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "Missing file in request"}), 400

    payroll_file = request.files['file']

    filename = secure_filename(payroll_file.filename)

    # app.logger.debug(filename)

    app.logger.info("upload payroll")

    status, msg,data = utils.read_file(payroll_file)
    # app.logger.info(data)
    status, msg,report_id = utils.get_report_id(filename)
    # app.logger.info(report_id)
    # model = PayrollReport()
    # conn = model.get_conn()
    status, msg, df = utils.parse_employee_logs(data, report_id)
    model.insert_csv(df, report_id)
    model.close_conn()
    return jsonify({"message": msg}), status



# Retrieve a report
@app.route("/payroll_report", methods = ["GET"])
def get_report():
    app.logger.info('get_report')
    rows = model.get_records()
    # for row in rows:
    #     app.logger.debug(row)
    status, payrollReport = utils.make_payroll_report(rows)
    # app.logger.debug(json.dumps(payrollReport, indent = 4))
    model.close_conn()
    return json.dumps(payrollReport)


# @app.errorhandler(404)
# def page_not_found(e):
#     return "<h1>404</h1><p>The resource could not be found.</p>", 404


app.run(debug = True)
