from contextlib import contextmanager
from models.taxi_model import TaxiTrips
import json
from sqlalchemy import inspect, func
from flask_sqlalchemy import SQLAlchemy
import os
from main import app

@contextmanager
def sql_session():
    db = SQLAlchemy()
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('POSTGRESS_CONNECTION_STRING')
    db.init_app(app)
    session = db.session()
    try:
        yield session
    finally:
        session.close()

def sql_get_all(limit) -> json:
    output = []
    with sql_session() as session:
        results = session.query(TaxiTrips).limit(limit).all()
        output.extend(iter(results))
    return json.dumps(output)

# def sql_get_summary(limit) -> None:
#     pass

# def sql_filter_by_equals_to(limit, column, value) -> json:
#     output = []
#     with sql_session() as session:
#         results = session.query(TaxiTrips).filter(getattr(TaxiTrips, column) == value).limit(limit).all()
#         output.extend(results)
#     return json.dumps(output)

# def sql_filter_by_greater_than(limit, column, value) -> json:
#     output = []
#     with sql_session() as session:
#         results = session.query(TaxiTrips).filter(getattr(TaxiTrips, column) > value).limit(limit).all()
#         output.extend(results)
#     return json.dumps(output)

# def sql_filter_by_less_than(limit, column, value) -> json:
#     output = []
#     with sql_session() as session:
#         results = session.query(TaxiTrips).filter(getattr(TaxiTrips, column) < value).limit(limit).all()
#         output.extend(results)
#     return json.dumps(output)
