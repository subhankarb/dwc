import csv
from flask import Flask, render_template, jsonify

DATE_DIR = 'data/'
DAILY_DATA_FILE = 'daily_price.csv'
MONTHLY_DATA_FILE = 'monthly_price.csv'
YEARLY_DATA_FILE = 'yearly_price.csv'

DAILY_DATA = list(csv.DictReader(open(DATE_DIR + DAILY_DATA_FILE)))
MONTHLY_DATA = list(csv.DictReader(open(DATE_DIR + MONTHLY_DATA_FILE)))
YEARLY_DATA = list(csv.DictReader(open(DATE_DIR + YEARLY_DATA_FILE)))

app = Flask(__name__)


@app.route("/data")
def data():
    return jsonify(DAILY_DATA)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()