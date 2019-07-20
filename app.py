"""
This simple API returns the upcoming holidays.
One limit to this API is that it only goes to the end of the year, but this could
be extended without many difficulties. The API can also be easily extended to vary
the number of holidays returned, as the functions in "holidays.py" allow for this
flexibility.

Author: Nav
Date: July 20th, 2019
"""

import flask
import json
import holidays

app = flask.Flask(__name__)

@app.route('/')
def index():
    return "<h1 style='text-align: center;'>Nerevu Internship Challenge</h1>"

@app.route('/holidays')
def return_holidays():
    """
    This function returns an array of dictionaries of the next holidays.
    It will check to see if "holidayType" was passed to the API. If it was,
    the returned results will only be of the specified holiday type if the
    type is valid.
    The federal example url: http://localhost:5000/holidays?holidayType=Federal%20Holiday
    """
    upcoming_holidays = []
    try:
        holiday_type = flask.request.args['holidayType']
    except:
        holiday_type = None

    number_of_holidays = 10
    upcoming_holidays = holidays.holidays(number_of_holidays, holiday_type)

    return json.dumps(upcoming_holidays)
