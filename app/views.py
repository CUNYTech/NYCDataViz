from flask import Flask

app = Flask(__name__)

from flask import render_template
from flask import Response
#<<<<<<< HEAD

from dateutil.relativedelta import *
from dateutil.parser import *

import requests

from datetime import *

#=======
from flask import jsonify
#>>>>>>> adding some stuff







"""
@app.route('/')
@app.route('/index.html')
def index():
    '''
    Returns a static webpage for now.
    '''
    return render_template('index.html')

#<<<<<<< HEAD

@app.route('/query/')
def request():
    # These are the desired columns:
    # ['Latitude', 'Longitude', 'Created Date', 'Agency', 'Agency Name', 'Complaint Type', 'Descriptor']
    columns = "latitude,longitude,created_date,agency,agency_name,complaint_type,descriptor"

    # Get recent service requests (last 6 weeks)
    today = date.today()
    six_weeks_ago = today - relativedelta(weeks=6)
    # Convert datetimes into Floating Timestamps for use with Socrata.
    today = today.strftime('%Y-%m-%d') + 'T00:00:00'
    six_weeks_ago = six_weeks_ago.strftime('%Y-%m-%d') + 'T00:00:00'

    '''
    GET request on Socrata's API.
    First part is the data set we're using.
    $limit is set to 500K, because we want 500K records.
    $select will select the columns we want, as defined earlier.
    $where allows us to choose the time frame. In this case it's 6 weeks.
    '''
    r = requests.get(
        "https://data.cityofnewyork.us/resource/fhrw-4uyv.json?" +
        "$limit=500000&$select={}&".format(columns) +
        "$where=created_date between \'{}\' and \'{}\' and longitude IS NOT NULL".format(six_weeks_ago, today)
    )

    # Create the response
    response = Response(response=r, status=200, mimetype='application/json')
    return response
@app.route('/request')
def request():
    #Use the make_request() function to get to data for
    req = make_request()
    return jsonify(req)
#>>>>>>> adding some stuff


"""
#===============================================================================
#function to fill the tables

def Get_request_Column(Column_name):
    '''
    Made the function smaller
    '''

    '''
    GET request on Socrata's API.
    First part is the data set we're using.
    $limit is set to 500K, because we want 500K records.
    $select will select the columns we want, as defined earlier.
    $where allows us to choose the time frame. In this case it's 6 weeks.
    '''
    today = date.today()
    six_weeks_ago = today - relativedelta(weeks=6)
    # Convert datetimes into Floating Timestamps for use with Socrata.
    today = today.strftime('%Y-%m-%d') + 'T00:00:00'
    six_weeks_ago = six_weeks_ago.strftime('%Y-%m-%d') + 'T00:00:00'
    r = requests.get(
        "https://data.cityofnewyork.us/resource/fhrw-4uyv.json?" +
        "$limit=10000&$select={}&".format(Column_name) +
        "$where=created_date between \'{}\' and \'{}\' and longitude IS NOT NULL".format(six_weeks_ago, today))

        #Might need this..
        #response = Response(response=r, status=200, mimetype='application/json')
    return r

#SQL stuff
from sqlalchemy import *
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

db = {'drivername': 'postgres', #I Heroku information
      'username': 'zqswoziimgfgiw',
      'password': 'a208273872dfe3ca8c742b5d61c493d3932cf30c4c61da3a5bf75805bce69dc0',
      'host': 'ec2-50-17-217-166.compute-1.amazonaws.com',
      'port': 5432}

url = URL(db)
engine = create_engine(url)

metadata = MetaData()
metadata.reflect(bind=engine)

def create_table(name, metadata):
    tables = metadata.tables.keys()
    if name not in tables:
        table = Table(name, metadata,
                      Column('latitude', Integer),
                      Column('longitude', Integer),
                      Column('created_date', String),
                      Column('agency', String),
                      Column('agency_name', Integer),
                      Column('complaint_type', String),
                      Column('descriptor', String))
        table.create(engine)

latitude_ = Get_request_Column('latitude')
longitude_ = Get_request_Column('longitude')
created_date_ = Get_request_Column('created_date')
agency_ = Get_request_Column('agency')
agency_name_ = Get_request_Column('agency_name')
complaint_type_ = Get_request_Column('complaint_type')
descriptor_ = Get_request_Column('descriptor')
# insert multiple data
conn.execute(table.insert(),[
   {'latitude':latitude_,'longitude':longitude_},
   {'created_date':created_date_,'agency':agency_},
   {'agency_name':agency_name_},{'complaint_type':complaint_type_},
   {'descriptor':descriptor_}])
