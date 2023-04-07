from main import db
from sqlalchemy import Column, String, Integer, Float
import os

class TaxiTrips(db.Model):
    __tablename__ = os.getenv('DATA_TABLE_NAME')
    unique_key = Column(String(20), primary_key=True, nullable=False, unique=True)
    taxi_id = Column(String(20), nullable=False)
    trip_start_timestamp = Column(String(30), nullable=False)
    trip_end_timestamp = Column(String(30), nullable=False)
    trip_seconds = Column(Integer, nullable=False)
    trip_miles = Column(Float, nullable=False)
    pickup_census_tract = Column(Float)
    dropoff_census_tract = Column(Float)
    pickup_community_area = Column(Float)
    dropoff_community_area = Column(Float)
    fare = Column(Float, nullable=False)
    tips = Column(Float)
    tolls = Column(Float)
    extras = Column(Float)
    trip_total = Column(Float, nullable=False)
    payment_type = Column(String(20), nullable=False)
    company = Column(String(50))
    pickup_latitude = Column(Float, nullable=False)
    pickup_longitude = Column(Float, nullable=False)
    pickup_location = Column(String(100))
    dropoff_latitude = Column(Float, nullable=False)
    dropoff_longitude = Column(Float, nullable=False)
    dropoff_location = Column(String(100))