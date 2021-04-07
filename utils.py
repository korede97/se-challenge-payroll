
from datetime import datetime, timedelta
# import datetime
import logging
import flask
import pandas as pd
import re
import json
from flask import jsonify, make_response
from calendar import monthrange
import collections



logging.basicConfig(level=logging.DEBUG)
app = flask.Flask(__name__)

def read_file(file):
    # filename = file.filename
    # report_id =
    data = pd.read_csv(file)
    app.logger.info("read file")
    # app.logger.info(data)
    return 200, "uploaded successfully", data


def check_csv_specification(data, filename):
    # ensure there is well-informed file name
    filename_split = re.findall('time-report-\d{2}',filename)
    if not filename_split:
        return False
    # ensure there is a well-informed headerline
    ideal_header = ['date', 'hours worked', 'employee id', 'job group']
    result = all(map(lambda x, y: x == y, data.columns, ideal_header))

    # app.logger.debug(result)
    if not result:
        return False

    return True

def get_report_id(filename):
    filename_split = re.findall('\d{2}',filename)
    report_id = int(filename_split[0])
    # app.logger.info(f'report_id: {report_id}')
    return 200, "retrived report id",report_id

# parse data
def parse_employee_logs(data, report_id):

    date = pd.to_datetime(data['date'])
    hours_worked = data['hours worked'].astype(float)
    employee_id = data['employee id'].astype(int)
    job_group = data['job group']

    df = pd.DataFrame({'date':date, 'employee_id':employee_id, 'hours_worked': hours_worked, 'job_group': job_group, 'report_id':report_id})

    return 200, "successfully parsed employee data", df

# Make a report detailing how much each employee should be paid in each pay period

def make_payroll_report(rows):

    temp_list = []
    for row in rows:
        employee_id = row["employee_id"]
        pay_period = get_pay_period(row['date'])
        end_date = pay_period["endDate"] # could use endDate or startDate..
        amount_paid = calculate_amount_paid(row['hours_worked'], row['job_group'])

        check_list = check_log_with_same_pay_period(temp_list, employee_id,end_date, amount_paid)
        if(check_list):
            temp_list = check_list
            continue

        temp_list.append({
            'employee_id':str(employee_id),
            'payPeriod':pay_period,
            'amountPaid': amount_paid
            }
        )

    # sorted by employee id and then pay period start
    # newlist = sorted(temp_list, key=itemgetter('employee_id', 'startDate'))
    employeeReports_list = sorted(temp_list, key=lambda x: (
            x['employee_id'],
            x['payPeriod']['startDate']
        )
    )

    payrollReport = {'payrollReport': {'employeeReports':employeeReports_list}}
    # app.logger.info(json.dumps(test_dict, indent = 4))

    return 200, payrollReport

def check_log_with_same_pay_period(curr_list, employee_id, end_date, amount_paid):
    check_list = curr_list.copy()
    for i in range(0,len(check_list)):
        curr_log = check_list[i]
        if int(curr_log['employee_id']) == employee_id:
            if curr_log["payPeriod"]["endDate"] == end_date:
                amount_1_str = curr_log["amountPaid"]
                amount_1_int = int(re.findall('\d+', amount_1_str)[0])
                amount_2_str = amount_paid
                amount_2_int = int(re.findall('\d+', amount_2_str)[0])
                tot_amount = amount_1_int + amount_2_int
                curr_log["amountPaid"] = "$"+"{:.2f}".format(tot_amount)
                return check_list
    return None


def get_pay_period(date_str):
    date_datetime = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    if 1 <= date_datetime.day <= 15:
        start_datetime = date_datetime.replace(day = 1)
        end_datetime = date_datetime.replace(day = 15)
        # end_date = datetime.date(start_datetime.year, start_datetime.month,15)
    elif 16 <= date_datetime.day <= 31:
        _,num_day=monthrange(date_datetime.year, date_datetime.month)
        start_datetime = date_datetime.replace(day = 16)
        end_datetime = date_datetime.replace(day = num_day)

    start_date = start_datetime.date()
    end_date = end_datetime.date()

    return {'startDate': start_date.strftime("%Y-%m-%d"), 'endDate': end_date.strftime("%Y-%m-%d")}

def calculate_amount_paid(hours_worked, job_group):
    if job_group == "A":
        return "$"+"{:.2f}".format((hours_worked*20))
        # return "$"+"%.2f"%(hours_worked*20)
    return "$"+"{:.2f}".format((hours_worked*30))
