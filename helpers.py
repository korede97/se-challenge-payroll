
from datetime import datetime, timedelta
# import datetime
import logging
import flask
import pandas as pd
import re
import sqlite3 as sql
import json
from flask import jsonify, make_response
from calendar import monthrange
from operator import itemgetter



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

def to_database(data, report_id):
    # parse data
    app.logger.info(f'type(date) \n {data.dtypes}')

    date = pd.to_datetime(data['date'])
    hours_worked = data['hours worked'].astype(float)
    employee_id = data['employee id'].astype(int)
    job_group = data['job group']
    # app.logger.info(f'date \n {date}')
    # app.logger.info(f'dtype(date) \n {date.dtype}')
    # app.logger.info(f'dtype(date) \n {date.dtype}')
    df_new = pd.DataFrame({'date':date, 'employee_id':employee_id, 'hours_worked': hours_worked, 'job_group': job_group, 'report_id':report_id})
    app.logger.info(f'df_new \n {df_new}')
    app.logger.info('before database connection')

    #insert in database
    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS t (
        report_id INTEGER,
        employee_id INTEGER,
        job_group TEXT,
        hours_worked INTEGER,
        date TEXT
    );""")

    # check if report_id already exists in database
    if(check_report_id_exsists(report_id)):
        app.logger.info('found existing report_id 2')
        return 400, "report id already exists"
    #
    # # add information to database...
    df_new.to_sql('t',conn, if_exists= 'replace', index = False)
    # cur.execute("INSERT INTO t (report_id, employee_id, job_group, hours_worked, date) VALUES (?,?,?,?,?)",(report_id[0],employee_id[0],job_group[0],hours_worked[0],date[0]) )
    conn.commit()

    cur.execute("SELECT * FROM t")
    rows = cur.fetchall()
    for row in rows:
        app.logger.info(row)

    conn.close()
    return 200, "to database successfull"



def check_report_id_exsists(report_id):
    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM t WHERE report_id =?", (report_id,))
    result = cur.fetchone()

    if(result):
        app.logger.info('found existing report_id 1')
        return True
    return False


# Make a report detailing how much each employee should be paid in each pay period

def make_payroll_report():
    conn = sql.connect("database.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM t")
    rows = cur.fetchall()

    temp = {}
    temp['payRollReport'] = {}
    temp_list = []
    for row in rows:
        # app.logger.info(row['employee_id'])
        # need to output employee_id as str but also need to sort ?
        temp_list.append({
            'employee_id':row["employee_id"],
            'payPeriod':get_pay_period(row['date']),
            'amountPaid': calculate_amount_paid(row['hours_worked'], row['job_group'])
            }
        )

    # newlist = sorted(temp_list, key=itemgetter('employee_id', 'startDate'))
    newlist = sorted(temp_list, key=lambda x: (
                    x['employee_id'],
                    x['payPeriod']['startDate']
                )
            )

    test_dict = {'payRollReport': {'employeeReports':newlist}}
    # app.logger.info(json.dumps(temp_list, indent = 4))
    app.logger.info(json.dumps(test_dict, indent = 4))


    return 200

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

    app.logger.debug(start_date)

    return {'startDate': start_date.strftime("%Y-%m-%d"), 'endDate': end_date.strftime("%Y-%m-%d")}

def calculate_amount_paid(hours_worked, job_group):
    if job_group == "A":
        return "$"+"{:.2f}".format((hours_worked*20))
        # return "$"+"%.2f"%(hours_worked*20)
    return "$"+"{:.2f}".format((hours_worked*30))
