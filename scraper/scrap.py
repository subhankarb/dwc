import requests
import os
import re
import collections
import arrow
import shutil
import csv
from bs4 import BeautifulSoup

__author__ = 'Subhankar Biswas'

URL = "http://www.eia.gov/dnav/ng/hist/rngwhhdd.htm"
REQUEST_HEADERS = {
    'Cache-Control': "no-cache",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch"
    }
DATE_DIR = '../data/'
DAILY_DATA_FILE = 'daily_price.csv'
MONTHLY_DATA_FILE = 'monthly_price.csv'
YEARLY_DATA_FILE = 'yearly_price.csv'


def get_gas_price():
    """

    """
    # response = requests.request("GET", URL, headers=REQUEST_HEADERS, stream=True)
    # response_page_soap = BeautifulSoup(response.text, 'html.parser')
    response_page_soap = BeautifulSoup(open('aa.html'), 'html.parser')
    table = response_page_soap.find('table', summary=re.compile("^Henry Hub Natural Gas Spot Price.*"))
    results = dict()
    headers = list()
    for row in table.findChildren('th'):
        headers.append(row.text.strip())
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        data = dict()
        if len(cells) is 6:
            for i in range(1, 6):
                data[headers[i]] = cells[i].text.strip()
            if cells[0].text is not None and cells[0].text != '':
                results[cells[0].text.strip()] = data
    return results


def generate_date(gas_price):
    """

    """
    data = dict()
    delta = {'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4}
    for price_key, price_value in gas_price.iteritems():
        start_date = price_key.strip().split('to')[0].strip()
        try:
            date = arrow.get(start_date, 'YYYY MMM-D')
        except Exception:
            date = arrow.get(start_date, 'YYYY MMM- D')
        for delta_key, delta_value in delta.iteritems():
            modified_date = date.replace(days=delta_value)
            if price_value[delta_key] != '':
                data[modified_date] = float(price_value[delta_key])
    return collections.OrderedDict(sorted(data.items()))


def aggregate_data(formatted_gas_price):
    """

    """
    final_data = dict()
    for date, value in formatted_gas_price.iteritems():
        dt = date.datetime
        year = dt.year
        month = dt.month
        day = dt.day
        if year not in final_data:
            final_data[year] = dict()
        if month not in final_data[year]:
            final_data[year][month] = dict()

        final_data[year][month][day] = value
    final_data = collections.OrderedDict(sorted(final_data.items()))
    return final_data


def write_daily_data(a):
    file_name = DATE_DIR + DAILY_DATA_FILE
    file_exists = os.path.isfile(file_name)
    headers = ['DAY', 'PRICE']
    with open(file_name, "wb") as c:
        writer = csv.writer(c, delimiter=',', lineterminator='\n')
        if not file_exists:
            writer.writerow(headers)
        for k, v in a.iteritems():
            writer.writerow([k.format('YYYY-MM-DD'), v])


def write_monthly_data(a):
    file_name = DATE_DIR + MONTHLY_DATA_FILE
    file_exists = os.path.isfile(file_name)
    headers = ['YEAR', 'MONTH', 'PRICE']
    total_data = []
    for year, v in a.iteritems():
        month_data = []
        for month, daily_values in v.iteritems():
            datas = daily_values.values()
            avg = round(sum(datas)/len(datas), 2)
            month_data.append([year, month, avg])
        total_data.extend(month_data)
    with open(file_name, "wb") as c:
        writer = csv.writer(c, delimiter=',', lineterminator='\n')
        if not file_exists:
            writer.writerow(headers)
        for d in total_data:
            writer.writerow(d)


def write_yearly_data(a):
    file_name = DATE_DIR + YEARLY_DATA_FILE
    file_exists = os.path.isfile(file_name)
    headers = ['YEAR', 'PRICE']
    total_data = []
    for year, v in a.iteritems():
        values = []
        for month, daily_values in v.iteritems():
            values.extend(daily_values.values())
        avg = round(sum(values)/len(values), 2)
        total_data.append([year, avg])
    print total_data
    with open(file_name, "wb") as c:
        writer = csv.writer(c, delimiter=',', lineterminator='\n')
        if not file_exists:
            writer.writerow(headers)
        for d in total_data:
            writer.writerow(d)

if __name__ == '__main__':
    shutil.rmtree(DATE_DIR, ignore_errors=True)
    os.makedirs(DATE_DIR)
    price = get_gas_price()
    formatted_price = generate_date(get_gas_price())
    aggregate_data = aggregate_data(formatted_price)
    write_daily_data(formatted_price)
    write_monthly_data(aggregate_data)
    write_yearly_data(aggregate_data)
    # for k, v in aggregate_data.iteritems():
    #     print k, '->', v
