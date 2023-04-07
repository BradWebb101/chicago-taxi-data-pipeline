from flask import Flask, request, jsonify, make_response
import os

from auth import authenticate
from sql_queries import sql_get_all, sql_get_summary, sql_filter_by_equals_to, sql_filter_by_greater_than, sql_filter_by_less_than
from dyanmo_queries import no_sql_get_all
from datetime import datetime
from parsing import to_csv

app = Flask(__name__)

@app.route('/')
def fetch_instructions():
    pass

@app.route('/all')
def fetch_all():
    access_key = request.headers.get('X-Access-Key')
    secret_key = request.headers.get('X-Secret-Key')
    limit = request.args.get('limit') or 1000
    source = request.args.get('source') or 'json'
    db = request.args.get('no_sql') or 'sql'

    if not authenticate(access_key, secret_key):
        return jsonify({'status_code': 401, 'results': 'Invalid credentials passed with request'})

    data = no_sql_get_all(limit) if db == 'no_sql' else sql_get_all(limit)

    if source == 'csv':
        response = make_response(to_csv(data))
        response.headers['Content-Disposition'] = f'attachment; filename=taxi_rides_data_out_{datetime.now}.csv'
        response.headers['Content-Type'] = 'text/csv'

    else:
        response = make_response(data)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'

    return {'status_code': 200, 'results': response}

# @app.route('/summary_stats')
# def fetch_summary():
#     access_key = request.headers.get('X-Access-Key')
#     secret_key = request.headers.get('X-Secret-Key')
#     limit = request.args.get('limit') or 1000
#     source = request.args.get('source') or 'json'
#     db = request.args.get('no_sql') or 'sql'

#     if not authenticate(access_key, secret_key):
#         return jsonify({'status_code': 401, 'data': 'Invalid credentials passed with request'})

#     data = no_sql_query(limit) if db == 'no_sql' else get_summary(limit)

# @app.route('/conditions')
# def fetch_summary():
#     access_key = request.headers.get('X-Access-Key')
#     secret_key = request.headers.get('X-Secret-Key')
#     limit = request.args.get('limit') or 1000
#     source = request.args.get('source') or 'json'
#     db = request.args.get('no_sql') or 'sql'
#     column_name=request.args.get('column_name')
#     filter_expression=request.args.get('filter_expression')
#     value=request.args.get('column_value')

#     if not authenticate(access_key, secret_key):
#         return jsonify({'status_code': 401, 'message': 'Invalid credentials passed with request'})
    
    
    

#     data = no_sql_query(limit) if db == 'no_sql' else count_by_column_where_equals(limit)

if __name__ == '__main__':
    app.run(debug=True)