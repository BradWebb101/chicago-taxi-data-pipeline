--Staging details
{% set staging_database_name = 'taxi_rides' %}
{% set staging_schema_name = 'staging' %}
{% set staging_table_name = 'taxi_rides_raw_json' %}
--Prod details 
{% set prod_database_name = 'taxi_rides' %}
{% set prod_schema_name = 'prod' %}
{% set prod_table_name = 'taxi_trips' %}


create or replace table taxi_rides.prod.taxi_trips as (
  with parsed_json as (
    select PARSE_JSON(JSON_DATA) as parsed from 
    "TAXI_RIDES"."STAGING"."TAXI_RIDES_RAW_JSON"),
  
  regex_replace as (
SELECT REGEXP_REPLACE(parsed, ':@', '') AS json_data
FROM parsed_json
  ),
  
  extracted_data as (SELECT 
      json_extract_path_text(json_data, 'trip_id')::VARCHAR(100) AS trip_id,
      json_extract_path_text(json_data, 'taxi_id')::VARCHAR(256) AS taxi_id,
      json_extract_path_text(json_data, 'trip_start_timestamp')::TIMESTAMP AS trip_start_timestamp,
      json_extract_path_text(json_data, 'trip_end_timestamp')::TIMESTAMP AS trip_end_timestamp,
      json_extract_path_text(json_data, 'trip_seconds')::INTEGER AS trip_seconds,
      json_extract_path_text(json_data, 'trip_miles')::FLOAT AS trip_miles,
      json_extract_path_text(json_data, 'pickup_census_tract')::VARCHAR(50) AS pickup_census_tract,
      json_extract_path_text(json_data, 'dropoff_census_tract')::VARCHAR(50) AS dropoff_census_tract,
      json_extract_path_text(json_data, 'pickup_community_area')::VARCHAR(50) AS pickup_community_area,
      json_extract_path_text(json_data, 'dropoff_community_area')::VARCHAR(50) AS dropoff_community_area,
      json_extract_path_text(json_data, 'fare')::FLOAT AS fare,
      json_extract_path_text(json_data, 'tips')::FLOAT AS tips,
      json_extract_path_text(json_data, 'tolls')::FLOAT AS tolls,
      json_extract_path_text(json_data, 'extras')::FLOAT AS extras,
      json_extract_path_text(json_data, 'trip_total')::FLOAT AS trip_total,
      json_extract_path_text(json_data, 'payment_type')::VARCHAR(50) AS payment_type,
      json_extract_path_text(json_data, 'company')::VARCHAR(50) AS company,
      json_extract_path_text(json_data, 'pickup_latitude')::FLOAT AS pickup_latitude,
      json_extract_path_text(json_data, 'pickup_longitude')::FLOAT AS pickup_longitude,
      ST_POINT(json_extract_path_text(json_data, 'pickup_centroid_location.coordinates[0]')::FLOAT, json_extract_path_text(json_data, 'pickup_centroid_location.coordinates[1]')::FLOAT) AS pickup_centroid_location,
      json_extract_path_text(json_data, 'dropoff_latitude')::FLOAT AS dropoff_latitude,
      json_extract_path_text(json_data, 'dropoff_longitude')::FLOAT AS dropoff_longitude,
      ST_POINT(json_extract_path_text(json_data, 'dropoff_centroid_location.coordinates[0]')::FLOAT, json_extract_path_text(json_data, 'dropoff_centroid_location.coordinates[1]')::FLOAT) AS dropoff_centroid_location
FROM 
    regex_replace),

existing_data as (
  select distinct(trip_id)
  from taxi_rides.prod.taxi_trips
),
    
new_data as (
  select * from extracted_data
  where trip_id not in (select distinct(trip_id) from taxi_rides.prod.taxi_trips)
)
  
 select * from new_data);