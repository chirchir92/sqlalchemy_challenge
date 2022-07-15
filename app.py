#****************start************************#
# import dependencies
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, false, func
import datetime as dt
import numpy as np

#------------------------------------------------------------
# database setup
engine=create_engine('sqlite:///resources/hawaii.sqlite')

# reflect the existing databse to a new model
base=automap_base()
# reflect tables
base.prepare(engine, reflect=True)
base.classes.keys()
# save references to the table
Measurement=base.classes.measurement
Station=base.classes.station
# create python sesseion link to the db
session=Session(engine)
# set up flask
app=Flask(__name__)
#------------------------------------------------------------------
# flask routes
@app.route('/')
def welcome():
    return(
        f'Routes are:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/start<br/>'
        f'/api/v1.0/start/end'
    )
#------------------------------------
@app.route('/api/v1.0/precipitation')
def precipitation():
    # Convert the query results to a dictionary using date as the key and prcp as the value.
    # query the dates and precipitation 
    results=session.query(Measurement.date,Measurement.prcp).all()
    session.close()
    
    precip=[]
    for result in results:
        prep_dict={}
        prep_dict['date']=result[0]
        prep_dict['prcp']=result[1]
        precip.append(prep_dict)
        
    return jsonify(precip)

#---------------------------------
@app.route('/api/v1.0/stations')
def stations():
    # query the stations names from the dataset
    results=session.query(Station.name).all()
    session.close()
    
    all_stations=list(np.ravel(results))
    return jsonify(all_stations)
#-----------------------------
@app.route('/api/v1.0/tobs')
def tobs():
    # query the dates, temps from the dataset
    # filter to get the stations with the most count (most active station)
    year_ago='2016-08-23'
    results=session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >=year_ago).\
            filter(Measurement.station=='USC00519281').all()   
    session.close()
    most_active=list(np.ravel(results))
    return jsonify(most_active)
#-------------------------------
@app.route('/api/v1.0/start')
def start():
    # define the first date of the trip
    # query the dataset and retun tmin. tavg and tmax from the dataset
    # only get data from the first day of the trip and later
    start_date='2016-01-02'
    results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
            group_by(Measurement.date).all()
    session.close()
    start=list(np.ravel(results))
    return jsonify(start)
#-------------------------------------
@app.route('/api/v1.0/start/end')
def end():
    # define the start and end dates of the trip
    # query the data and find temps(min, avg, max) from the dataset
    # filter the query to only get trip time data
    start_date='2016-01-02'
    end_date='2016-01-22'
    results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date<= end_date).\
            group_by(Measurement.date).all()
    session.close()
    end=list(np.ravel(results))
    return jsonify(end)
#-------------------------
if __name__ == '__main__':
    app.run(debug=True)
#***********end******************#
