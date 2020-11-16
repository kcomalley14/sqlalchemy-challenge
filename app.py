import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Setup Database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect existing database into new model
Base = automap_base()
# reflect tables found
Base.prepare(engine, reflect=True)

# References for each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# table = Station.__table__.columns.keys()
# print(table)

# Flask Setup
app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome():
    return (
            f"Welcome to my SQL-Alchemy Hawaii Climate APP API!<br/>"
            f"Available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
            f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session link from Python to DB
    session = Session(engine)

    # Query all precipitation data
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-24").all()
    
    session.close()

    # Convert list to Dictionary using date and prcp
    prcp_final = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp

        prcp_final.append(prcp_dict)
    
    return jsonify(prcp_final)

@app.route("/api/v1.0/stations")
def station():
    # Create session link from Python to DB
    session = Session(engine)

    # Query all station data
    results = session.query(Station.station).\
        order_by(Station.station).all()
    
    session.close()
    
    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temp_obs():
    # Create session link from Python to DB
    session = Session(engine)

    # Query all temp_obs data
    results = session.query(Measurement.date, Measurement.tobs, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-23").\
        filter(Measurement.station == "USC00519281").\
        order_by(Measurement.date).all()
    
    session.close()

    tobs_final = []
    for tobs, date, prcp in results:
        tobs_dict = {}
        tobs_dict["tobs"] = tobs
        tobs_dict["date"] = date
        tobs_dict["prcp"] = prcp

        tobs_final.append(tobs_dict)

    return jsonify(tobs_final)

@app.route("/api/v1.0/<start>")
def Start_date(start):
        # Create session link from Python to DB
    session = Session(engine)

    # Query all temp_obs data
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    session.close()

    start_tobs = []
    for min, max, avg in results:
        start_tobs_dict = {}
        start_tobs_dict['min_temp'] = min
        start_tobs_dict['max_temp'] = max
        start_tobs_dict['avg_temp'] = avg
        start_tobs.append(start_tobs_dict)

    return jsonify(start_tobs)

@app.route("/api/v1.0/<start>/<end>")
def Start_end_date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    # Query all tobs data between dates

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()
  
    # Create a dictionary from the row data and append to a list of start_end_date_tobs
    start_end_tobs = []
    for min, avg, max in results:
        start_end_tobs_dict = {}
        start_end_tobs_dict["min_temp"] = min
        start_end_tobs_dict["avg_temp"] = avg
        start_end_tobs_dict["max_temp"] = max
        start_end_tobs.append(start_end_tobs_dict) 
    

    return jsonify(start_end_tobs)


if __name__ == "__main__":
    app.run(debug=True)
