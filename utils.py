
from datetime import datetime, timedelta
# import datetime
import logging
import flask
import pandas as pd
import re
# import sqlite3 as sql
import json
from flask import jsonify, make_response
from calendar import monthrange
# from operator import itemgetter


logging.basicConfig(level=logging.DEBUG)
app = flask.Flask(__name__)

def read_file(file):
    # filename = file.filename
    # report_id =
    data = pd.read_csv(file)
    app.logger.info("read file")
    # app.logger.info(data)
    return 200, "uploaded successfully", data

def get_report_id(filename):
    filename_split = re.findall('\d{2}',filename)
    # filename_split = file.split(["-","."])
    report_id = int(filename_split[0])
    app.logger.info(f'report_id: {report_id}')
    return 200, "retrived report id",report_id

def parse_employee_logs(data, report_id):
    # parse data
    # app.logger.debug(f'type(date) \n {data.dtypes}')

    date = pd.to_datetime(data['date'])
    hours_worked = data['hours worked'].astype(float)
    employee_id = data['employee id'].astype(int)
    job_group = data['job group']


    df = pd.DataFrame({'date':date, 'employee_id':employee_id, 'hours_worked': hours_worked, 'job_group': job_group, 'report_id':report_id})
    # app.logger.debug(f'df_ \n {df}')

    return 200, "successfully parsed employee data", df


# Make a report detailing how much each employee should be paid in each pay period

def make_payroll_report(rows):
    # conn = sql.connect("payroll.db")
    temp_list = []
    for row in rows:
        temp_list.append({
            'employee_id':str(row["employee_id"]),
            'payPeriod':get_pay_period(row['date']),
            'amountPaid': calculate_amount_paid(row['hours_worked'], row['job_group'])
            }
        )

    # newlist = sorted(temp_list, key=itemgetter('employee_id', 'startDate'))
    employeeReports_list = sorted(temp_list, key=lambda x: (
            x['employee_id'],
            x['payPeriod']['startDate']
        )
    )

    payrollReport = {'payRollReport': {'employeeReports':employeeReports_list}}
    # app.logger.info(json.dumps(test_dict, indent = 4))

    return 200, payrollReport

def get_pay_period(date_str):
    start_datetime = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    if 1 <= start_datetime.day <= 15:
        end_datetime = start_datetime.replace(day=15)
        # end_date = datetime.date(start_datetime.year, start_datetime.month,15)
    elif 16 <= start_datetime.day <= 31:
        _,day=monthrange(start_datetime.year, start_datetime.month)
        end_datetime = start_datetime.replace(day = day)

    start_date = start_datetime.date()
    end_date = end_datetime.date()

    return {'startDate': start_date.strftime("%Y-%m-%d"), 'endDate': end_date.strftime("%Y-%m-%d")}

def calculate_amount_paid(hours_worked, job_group):
    if job_group == "A":
        return "$"+"{:.2f}".format((hours_worked*20))
        # return "$"+"%.2f"%(hours_worked*20)
    return "$"+"{:.2f}".format((hours_worked*30))
