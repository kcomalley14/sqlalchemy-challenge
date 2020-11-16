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
#tables = engine.table_names()
#print(tables)

# References for each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome
