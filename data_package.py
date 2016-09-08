import datapackage
import shutil
import os
import io
import csv
from jsontableschema import infer

__author__ = 'z001h2s'

CSV_DATE_DIR = './data/'
PKG_DATE_DIR = './pkg/'
DAILY_DATA_FILE_CSV = 'daily_price.csv'
DAILY_DATA_FILE_PKG = 'daily_price.json'
MONTHLY_DATA_FILE_CSV = 'monthly_price.csv'
MONTHLY_DATA_FILE_PKG = 'monthly_price.json'
YEARLY_DATA_FILE_CSV = 'yearly_price.csv'
YEARLY_DATA_FILE_PKG = 'yearly_price.json'
# dp = datapackage.DataPackage()
# dp.descriptor['name'] = 'period-table'
# dp.descriptor['title'] = 'Periodic Table'


def package_daily_data():
    csv_file_path = CSV_DATE_DIR + DAILY_DATA_FILE_CSV
    pkg_file_path = PKG_DATE_DIR + DAILY_DATA_FILE_PKG
    dp = datapackage.DataPackage()
    dp.descriptor['name'] = 'daily-gas-price'
    dp.descriptor['title'] = 'Daily Gas Price'
    with io.open(csv_file_path) as stream:
        headers = stream.readline().rstrip('\n').split(',')
        values = csv.reader(stream)
        schema = infer(headers, values)
        dp.descriptor['resources'] = [
            {
                'name': 'data',
                'path': csv_file_path,
                'schema': schema
            }
        ]
    with open(pkg_file_path, 'w') as f:
        f.write(dp.to_json())


def package_monthly_data():
    csv_file_path = CSV_DATE_DIR + MONTHLY_DATA_FILE_CSV
    pkg_file_path = PKG_DATE_DIR + MONTHLY_DATA_FILE_PKG
    dp = datapackage.DataPackage()
    dp.descriptor['name'] = 'monthly-gas-price'
    dp.descriptor['title'] = 'Monthly Avg Gas Price'
    with io.open(csv_file_path) as stream:
        headers = stream.readline().rstrip('\n').split(',')
        values = csv.reader(stream)
        schema = infer(headers, values)
        dp.descriptor['resources'] = [
            {
                'name': 'data',
                'path': csv_file_path,
                'schema': schema
            }
        ]
    with open(pkg_file_path, 'w') as f:
        f.write(dp.to_json())


def package_yearly_data():
    csv_file_path = CSV_DATE_DIR + YEARLY_DATA_FILE_CSV
    pkg_file_path = PKG_DATE_DIR + YEARLY_DATA_FILE_PKG
    dp = datapackage.DataPackage()
    dp.descriptor['name'] = 'yearly-gas-price'
    dp.descriptor['title'] = 'Yearly Avg Gas Price'
    with io.open(csv_file_path) as stream:
        headers = stream.readline().rstrip('\n').split(',')
        values = csv.reader(stream)
        schema = infer(headers, values)
        dp.descriptor['resources'] = [
            {
                'name': 'data',
                'path': csv_file_path,
                'schema': schema
            }
        ]
    with open(pkg_file_path, 'w') as f:
        f.write(dp.to_json())

if __name__ == '__main__':
    shutil.rmtree(PKG_DATE_DIR, ignore_errors=True)
    os.makedirs(PKG_DATE_DIR)
    package_daily_data()
    package_monthly_data()
    package_yearly_data()

