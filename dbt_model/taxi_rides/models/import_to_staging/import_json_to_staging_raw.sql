-- models/my_project/create_db_schema_table.sql
{% set database_name = 'taxi_rides' %}
{% set schema_name = 'staging' %}
{% set table_name = 'taxi_rides_raw_json' %}

-- Copy data into table from file
copy into {{database_name}}.{{schema_name}}.{{table_name}}
from @IMPORT_RAW_JSON
file_format=(TYPE='JSON' STRIP_OUTER_ARRAY=TRUE)