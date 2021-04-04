
from datetime import datetime
# import datetime
import logging
import flask
import pandas as pd
import re
import sqlite3 as sql
from flask import jsonify, make_response

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
# def make_report():
