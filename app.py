# 9.5.1
# import dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# set up database
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect the database into our classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# create a variable for each of the classes
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database
session = Session(engine)

# create Flask application called app
app = Flask(__name__)
@app.route("/")

# create a function welcome() with a return statement
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!<br />
    Available Routes:<br />
    /api/v1.0/precipitation<br />
    /api/v1.0/stations<br />
    /api/v1.0/tobs<br />
    /api/v1.0/temp/start/end<br />
    
    ''')

# 9.5.3
# precipitation route
@app.route("/api/v1.0/precipitation")
# create precipitatio function
def precipitation():
    # one year ago from the most recent date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # get the date and precipitation for the previous year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    # use jsonify() to format our results into a JSON structured file
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# 9.5.4
# Stations Route
@app.route("/api/v1.0/stations")
# create new function "stations"
def stations():
    # get all stations from db
    results = session.query(Station.station).all()
    # extract results into array, convert into list.
    stations = list(np.ravel(results))
    # jsonify the list and return it as JSON
    return jsonify(stations=stations)

# 9.5.5
# Temperature Route
@app.route("/api/v1.0/tobs")
# create new function "temperature"
def temp_monthly():
    # calculate the date one year ago from the last date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # to query the primary station for all the temperature observations from the previous year.
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    # unravel the results into a one-dimensional array and convert that array into a list
    temps = list(np.ravel(results))
    # jsonify the list and return our results
    return jsonify(temps=temps)

# 9.5.6
# Statistics Route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
# create a function called stats() to put our code in
def stats(start=None, end=None):
    # reate a query to select the minimum, average, and maximum temperatures from our SQLite database
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        # unravel the results into a one-dimensional array and convert them to a list
        temps = list(np.ravel(results))
        # jsonify our results and return them.
        return jsonify(temps=temps)
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
