import flask
from flask import request, jsonify
import os
import sqlite3 as sql
import pandas as pd
import logging
import helpers

logging.basicConfig(level=logging.DEBUG)

app = flask.Flask(__name__)

app.config["DEBUG"] = True

# @app.route("/", methods=["GET", "POST"])
# def index():
#     return render_template("upload.html")


@app.route("/", methods=["POST","GET"])
def home():
    app.logger.info("Hello world - app.logger.info")
    return "<h1> Payroll API...<h1>"

#
# @app.route("/api/payroll")
# def payroll_api():
#     conn = sqlite3.connect("employee_hours")
#     cur = conn.cursor()
#
#     results = cur.execute('SELECT * FROM books;').fetchall()
#     # result = [ {'report_id': report_id, 'employee_id': employee_id, 'period': period, 'amount': amount} for report_id, employee_id, period, amount in c.execute('SELECT * FROM report') ]
#
#     conn.close()
#     return jsonify(result)
#     return
#
#
# Upload a CSV file containing data on the number of hours worked per day per employee
@app.route("/upload_payroll", methods=['POST'])
def upload_file():
    payroll_file = request.files['file']
    app.logger.info("Hello world - app.logger.info")
    payroll_data = helpers.read_file(payroll_file)
    # timekeeping = helpers.get_timekeeping(payroll_api)
    # if(check_report_id_exsists):
    #     error = {"reason"}
        # res = make_response(,400)
        # return res
    # logging.debug("this is a debug message")
    # add information to database...
    # db.session(add.timekeeping)
    # print("hello", file = sys.stderr)
#
    return 200

# # Retrieve a report
# @app.route("/report", methods = ["GET"])
# def get_report():
#     payrollReport = helpers.make_report(con)
#     return
#
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


app.run(debug = True)
