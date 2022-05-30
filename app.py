# Step 2 - Climate App

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Use Flask `jsonify` to convert API data into a valid JSON response object.
from flask import Flask, jsonify
import json

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
        f"<a href = "/api/v1.0/precipitation">precipitation_api</a><br/>"
        f"<a href = "/api/v1.0/station">station_api</a><br/>"
        f"<a href = "/api/v1.0/tobs">tobs_api</a><br/>"
        f"/api/v1.0/start_date:<br/>"
        f"/api/v1.0/start_date/end_date:<br/>"
    )

# * `/api/v1.0/precipitation`
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Returns all recorded values of precipitation for all dates listed."""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
    
    prcp_query = session.query(measurement.prcp, measurement.date).all()
    data_dict = {}
    for row in prcp_query:
        prcp = row[0]
        date = row[1]
        data_dict[date] = prcp
    
    session.close()
        
    # Return the JSON representation of your dictionary.
    return jsonify(precipitation)

# * `/api/v1.0/stations`
@app.route("/api/v1.0/stations")
def stations():
    """Returns all recorded values of stations for all dates listed.
    Return a JSON list of stations from the dataset."""
    # Create our session (link) from Python to the DB
    session = Session(engine)

# * `/api/v1.0/tobs`
@app.route("/api/v1.0/tobs")
def tobs():
    """Query the dates and temperature observations of the most active
     station for the last year of data.."""
    # Create our session (link) from Python to the DB
    session = Session(engine)





if __name__ == "__main__":
    app.run(debug=True)

#   * Return a JSON list of temperature observations (TOBS) for the previous year.

# * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

#   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

#   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

#   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

# ## Hints

# * You will need to join the station and measurement tables for some of the queries.