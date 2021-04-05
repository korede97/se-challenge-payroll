# import flask
from flask import Flask, request, jsonify, make_response
from werkzeug.utils import secure_filename

import os
import sqlite3 as sql
import pandas as pd
import logging
import helpers

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# app.config["DEBUG"] = True

# @app.route("/", methods=["GET", "POST"])
# def index():
#     return render_template("upload.html")

@app.route('/')
def hello():
    return 'Hello, World!'
# @app.route("/")
# def home():
#     response = jsonify('Hello World!!!')
#     response.status_code = 200
#     return response

# @app.route('/')
# def index():
#     return jsonify({'hello': 'world'})


# @app.route("/", methods=['GET','POST'])
# def home():
#     return "Payroll API..."

#
# @app.route("/api/payroll")
# def payroll_api():
    # conn = sqlite3.connect("database.db")
    #
    # cur = conn.cursor()
    #
    # results = cur.execute('SELECT * FROM books;').fetchall()
    # # result = [ {'report_id': report_id, 'employee_id': employee_id, 'period': period, 'amount': amount} for report_id, employee_id, period, amount in c.execute('SELECT * FROM report') ]
    #
    # conn.close()
#     return jsonify(result)
#     return
#
#
# Upload a CSV file containing data on the number of hours worked per day per employee
@app.route("/upload_payroll", methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "Missing file in request"}), 400

    payroll_file = request.files['file']

    filename = secure_filename(payroll_file.filename)

    # app.logger.debug(filename)

    app.logger.info("upload payroll")

    status, msg,data = helpers.read_file(payroll_file)
    # app.logger.info(data)
    status, msg,report_id = helpers.get_report_id(filename)
    # app.logger.info(report_id)
    status, msg = helpers.to_database(data, report_id)
    return jsonify({"message": msg}), status



# Retrieve a report
@app.route("/payroll_report", methods = ["GET"])
def get_report():
    payrollReport = helpers.make_payroll_report(con)
    return jsonify(payrollReport)


# @app.errorhandler(404)
# def page_not_found(e):
#     return "<h1>404</h1><p>The resource could not be found.</p>", 404


app.run(debug = True)
