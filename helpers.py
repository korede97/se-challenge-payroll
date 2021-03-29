
from datetime import datetime
import logging
import flask
import pandas as pd
logging.basicConfig(level=logging.DEBUG)
app = flask.Flask(__name__)

def read_file(file):
    # filename = file.filename
    # report_id =
    data = pd.read_csv(file)
    app.logger("read csv")
    # app.logger.info(data)
    return data

# def check_report_id_exsists():
    # session = dbh()
    # if session.query(Reports).filter(Reports.id == report_id).count():
    # return True


# Make a report detailing how much each employee should be paid in each pay period
# def make_report():
