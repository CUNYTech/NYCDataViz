from app import app

from flask import render_template, Response, request

import pytz
from datetime import *
from dateutil.relativedelta import *
from dateutil.parser import *

import requests
import os


from flask import jsonify
@app.route('/')
@app.route('/index.html')
def index():
    '''
    Returns a static webpage for now.
    '''
    return render_template('index.html')

@app.route('/map.html')
def map():
    return render_template('map.html')



@app.route('/query')
def request_data():
    # These are the desired columns:
    # ['Unique Key', 'Latitude', 'Longitude', 'Created Date', 'Agency', 'Agency Name', 'Complaint Type', 'Descriptor']
    columns = "unique_key,latitude,longitude,created_date,agency,agency_name,complaint_type,descriptor"

    # Get recent service requests
    eastern_tz = pytz.timezone('US/Eastern')  # Generate time zone from string.
    today = datetime.now()  # Generate datetime object right now.
    today = today.astimezone(eastern_tz)  # Convert today to new datetime
    time_delta = today - relativedelta(days=3)
    # Convert datetimes into Floating Timestamps for use with Socrata.
    today = today.strftime('%Y-%m-%d') + 'T00:00:00'
    time_delta = time_delta.strftime('%Y-%m-%d') + 'T00:00:00'

    '''
    GET request on Socrata's API.
    First part is the data set we're using.
    $limit is set to the maximum number of records we want.
    $select will select the columns we want, as defined earlier.
    $where allows us to choose the time frame. In this case it's 6 weeks.
    '''
    r = requests.get(
        "https://data.cityofnewyork.us/resource/fhrw-4uyv.json?" +
        "$limit=500000&$select={}&".format(columns) +
        "$where=created_date between \'{}\' and \'{}\' and longitude IS NOT NULL".format(time_delta, today)
    )

    # Create the response
    response = Response(response=r, status=200, mimetype='application/json')
    return response



@app.route('/business')
def request_business_data():
    url = 'https://api.foursquare.com/v2/venues/explore'

    params = {
    'client_id' : os.environ['FOURSQUARE_CLIENT_ID'],
    'client_secret' : os.environ['FOURSQUARE_CLIENT_SECRET'],
        'v': '20170801',
        'll' : '40.7243,-74.0018',
        'query' :'coffee',
        'limit': '1'
        }
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    return jsonify(data)
