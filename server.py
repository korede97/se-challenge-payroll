import flask
from flask import request, jsonify
import sqlite3 as sql

app = flask.Flask(__name__)
app.config["DEBUG"] = True



@app.route("/", methods=["GET"])

def home():
  return "<h1> Payroll API...<h1>"





@app.route("/api/payments")
def payroll_api():
    return


# Upload a CSV file containing data on the number of hours worked per day per employee
@app.route("/upload", methods=['POST'])
def upload_file():
    return

# Retrieve a report detailing how much each employee should be paid in each pay period
@app.route("/report", methods = ["GET"])
def get_report():
    return


    
app.run()
