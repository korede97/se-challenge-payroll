import sqlite3 as sqlite3
import logging
import flask

app = flask.Flask(__name__)

class PayrollReport():

    def __init__(self, db):
        self.db = db
        conn = sqlite3.connect(db + ".db")
        self.conn = conn
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS employee_logs (
            report_id INTEGER,
            employee_id INTEGER,
            job_group TEXT,
            hours_worked INTEGER,
            date TEXT
        );""")
        conn.commit()
        conn.close()

    #update database
    def insert_csv(self, df, report_id):
        conn = self.get_conn()
        # cur.execute("INSERT INTO t (report_id, employee_id, job_group, hours_worked, date) VALUES (?,?,?,?,?)",(report_id,employee_id,job_group,hours_worked,date) )
        if(self.check_report_id_exsists(report_id)):
            return 400, "report id already exists"
        df.to_sql('employee_logs',conn, if_exists= 'append', index = False)
        conn.commit()
        return 200, "Updated table"

    # check if report_id already exists in database
    def check_report_id_exsists(self, report_id):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM employee_logs WHERE report_id =?", (int(report_id),))
        result = cur.fetchone()

        if(result):
            return True
        return False

    # retrieve data from database
    def get_logs(self):
        app.logger.info('get_records')
        conn = self.get_conn()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM employee_logs")
        rows = cur.fetchall()
        conn.commit()
        # conn.close()

        return rows

    def get_conn(self):
        return sqlite3.connect(self.db + ".db")

    def close_conn(self):
        self.conn.close()
