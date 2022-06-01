# Step 2 - Climate App
########################################################

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#########################################################

# Use Flask `jsonify` to convert API data into a valid 
# JSON response object.
from flask import Flask, jsonify

# Database Setup
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Flask Setup --> Create an app, being sure to pass __name__
app = Flask(__name__)

# Flask Routes
@app.route("/")
def Home_Page():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<a href = /api/v1.0/precipitation>Precipitation API</a><br/>"
        f"<a href = /api/v1.0/station>Stations API</a><br/>"
        f"<a href = /api/v1.0/tobs>Temperature API</a><br/>"
        f"/api/v1.0/start:<br/>"
        f"/api/v1.0/start/end:<br/>"
    )

# * `/api/v1.0/precipitation`
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Returns all recorded values of precipitation for all dates listed."""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Convert the query results to a dictionary using `date` 
    # as the key and `prcp` as the value.
    prcp_query = session.query(measurement.prcp, measurement.date).all()
    
    session.close()

    prcp_dict = {}
    for row in prcp_query:
        prcp = row[0]
        date = row[1]
        prcp_dict[date] = prcp 

    # Return the JSON representation of your dictionary.
    return jsonify(prcp_dict)

# * `/api/v1.0/stations`
@app.route("/api/v1.0/station")
def stations():
    """Returns all recorded values of stations for all dates listed.
    Return a JSON list of stations from the dataset."""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    station_list = [station.station,station.name,station.latitude,station.longitude,station.elevation]
    station_query = session.query(*station_list).all()
    session.close()

    stations = []
    for row in station_query:
        station_dict = {
        'station': row.station,
        'name': row.name,
        'latitude': row.latitude,
        'longitude': row.longitude,
        'elevation': row.elevation,
        }
        stations.append(station_dict)
    
    # Return the JSON representation of your dictionary.
    return jsonify(stations)

# * `/api/v1.0/tobs`
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of temperature observations (TOBS) for the previous year."""
    # Create our session (link) from Python to the DB
    session = Session(engine)
       
    date_year_prior = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    last_years_temps = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= date_year_prior).\
        order_by(measurement.station).all()    
   
    print(last_years_temps)
              
    session.close()

    tobs_dict = {}
    for row in last_years_temps:
        tobs = row[1]
        date = row[0]
        tobs_dict[date] = tobs
            
    # Return the JSON representation of your dictionary.
    return jsonify(tobs_dict)

# * `/api/v1.0/<start>
#   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>")
def tobs_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    tobsresults=session.query(func.min(measurement.tobs),func.avg(measurement.tobs),\
        func.max(measurement.tobs)),filter(measurement.date >= start).all()    
    
    session.close()

    tobstart = []
    for min,avg,max in tobsresults:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobstart.append(tobs_dict)
   
    return jsonify(tobstart)

# * `/api/v1.0/<start>/<end>`
#   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def tobs_start_end(start_end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    tobsresults=session.query(func.min(measurement.tobs),func.avg(measurement.tobs),\
        func.max(measurement.tobs)),filter(measurement.date >= start),\
        filter(measurement.date <= end).all()    
    
    session.close()

    tobstartend = []
    for min,avg,max in tobsresults:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobstartend.append(tobs_dict)
   
    return jsonify(tobstartend)

if __name__ == "__main__":
    app.run(debug=True)