# Import the dependencies.

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(autoload_with=engine)

# reflect the tables
Base.classes.keys()

# Save references to each table
Measurements = Base.classes.measurement
Stations = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine) 

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
# State the available routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Enter the date in the format yyyy-mm-dd instead of start/end '<br/>"
        f"/api/v1.0/start <br>"
        f"/api/v1.0/start/end"
        )
#################################################
# for all the routes decorators and functions will be used
# Precipitation Route

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    recent_date = datetime.strptime('2017-08-23', "%Y-%m-%d")
# Calculate the date one year from the last date in data set.
    one_year_from_last_date = recent_date - timedelta(days=366)
# Perform a query to retrieve the data and precipitation scores
    prcp_summary = session.query(Measurements.date, Measurements.prcp).\
                  filter(Measurements.date > one_year_from_last_date).all()
    session.close()
#create an empty list to get all the key value pairs from the above query results by looping and appending the list
    prcp_list = []
    for date, prcp in prcp_summary.items():
    prcp_list.append((date, prcp))

    return jsonify(prcp_list)

#################################################
# Station Route
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stn_summary = session.query(Stations.station,Stations.name).all()
    session.close()
    #create an empty list to get all the key value pairs from the above query results by looping and appending the list
    stn_list = []
    for station,name in stn_summary:
    stn_list.append((station,name))

    return jsonify(stn_list)

#################################################
# Tobs Route 
@app.route("/api/v1.0/tobs")
def tobs():
    recent_date = datetime.strptime('2017-08-23', "%Y-%m-%d")
    # Calculate the date one year from the last date in data set.
    one_year_from_last_date = recent_date - timedelta(days=366)
    session = Session(engine)
    tobs_summary = session.query(Measurements.date,Measurements.tobs).\
        filter(Measurements.station == 'USC00519281').filter(Measurements.date > query_date).all()
    session.close()
    #create an empty list to get all the key value pairs from the above query results by looping and appending the list
    tobs_list = []
    for date,tobs in tobs_summary:
    tobs_list.append((date,tobs))
    
    return jsonify(tobs_list)

#################################################
# start and start/end route
@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    tobs_start = session.query(func.min(Measurements.tobs),\
                                func.max(Measurements.tobs),func.avg(Measurements.tobs)).filter(Measurements.date>=start).all()
    session.close()
    tobs_start_list = []
    min_tobs = min(tobs_start)
    max_tobs = max(tobs_start)
    avg_tobs = sum(tobs_start) / len(tobs_start)
    
    return jsonify(tobs_start_list)

#create an empty list to get all the key value pairs from the above query results by looping and appending the list

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):
    session = Session(engine)
    tobs_start_end = session.query(func.min(Measurements.tobs),\
                                func.max(Measurements.tobs),func.avg(Measurements.tobs)).\
                                filter(Measurements.date>=start).filter(Measurements.date<=end).all()
    session.close()
    tobs_start_end_list = []
    min_tobs = min(tobs_start_end)
    max_tobs = max(tobs_start_end)
    avg_tobs = sum(tobs_start_end) / len(tobs_start_end)
    
    return jsonify(tobs_start_end_list)

if __name__ == '__main__':
    app.run(debug=True)