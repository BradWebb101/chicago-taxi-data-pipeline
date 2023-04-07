import boto3
import json
import jsonschema
from jsonschema import validate
import os

# Define the JSON schema for validation
schema = {
    "title": "Chicago Taxi Rides Schema",
    "description": "Schema for the Chicago Taxi Rides dataset.",
    "type": "object",
    "properties": {
        "unique_key": {
            "type": "string",
            "description": "Unique identifier for each taxi ride"
        },
        "taxi_id": {
            "type": "string",
            "description": "Unique identifier for the taxi cab"
        },
        "trip_start_timestamp": {
            "type": "string",
            "format": "date-time",
            "description": "Start time of the trip in ISO 8601 format"
        },
        "trip_end_timestamp": {
            "type": "string",
            "format": "date-time",
            "description": "End time of the trip in ISO 8601 format"
        },
        "trip_seconds": {
            "type": "integer",
            "description": "Duration of the trip in seconds"
        },
        "trip_miles": {
            "type": "number",
            "description": "Distance of the trip in miles"
        },
        "pickup_census_tract": {
            "type": "string",
            "description": "Census tract of the pickup location"
        },
        "dropoff_census_tract": {
            "type": "string",
            "description": "Census tract of the dropoff location"
        },
        "pickup_community_area": {
            "type": "integer",
            "description": "Community area of the pickup location"
        },
        "dropoff_community_area": {
            "type": "integer",
            "description": "Community area of the dropoff location"
        },
        "fare": {
            "type": "number",
            "description": "Fare amount charged for the trip"
        },
        "tips": {
            "type": "number",
            "description": "Tip amount charged for the trip"
        },
        "tolls": {
            "type": "number",
            "description": "Toll amount charged for the trip"
        },
        "extras": {
            "type": "number",
            "description": "Extra charges for the trip (such as fuel surcharge)"
        },
        "trip_total": {
            "type": "number",
            "description": "Total amount charged for the trip"
        },
        "payment_type": {
            "type": "string",
            "description": "Payment type (Cash, Credit Card, etc.)"
        },
        "company": {
            "type": "string",
            "description": "Name of the taxi company"
        },
        "pickup_latitude": {
            "type": "number",
            "description": "Latitude of the pickup location"
        },
        "pickup_longitude": {
            "type": "number",
            "description": "Longitude of the pickup location"
        },
        "dropoff_latitude": {
            "type": "number",
            "description": "Latitude of the dropoff location"
        },
        "dropoff_longitude": {
            "type": "number",
            "description": "Longitude of the dropoff location"
        }
    },
    "required": [
        "unique_key",
        "taxi_id",
        "trip_start_timestamp",
        "trip_end_timestamp",
        "trip_seconds",
        "trip_miles",
        "fare",
        "trip_total",
        "payment_type",
        "pickup_latitude",
        "pickup_longitude",
        "dropoff_latitude",
        "dropoff_longitude"]}


# Initialize the DynamoDB client and resource
dynamodb = boto3.client('dynamodb')
dynamodb_resource = boto3.resource('dynamodb')

# Define the DynamoDB tables
data_table = dynamodb_resource.Table(os.getenv('PASSED_VALIDATION_TABLE'))
failed_table = dynamodb_resource.Table(os.getenv('FAILED_VALIDATION_TABLE'))

def handler(event, context):
    # Read in the JSON file from S3
    s3 = boto3.resource('s3')
    bucket = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']
    file = s3.Object(bucket, file_name)
    data = json.loads(file.get()['Body'].read().decode('utf-8'))

    for row in data:
        try:
            # Validate the data against the JSON schema
            validate(instance=row, schema=schema)
            
            # If validation passes, add the data to the data table
            data_table.put_item(Item=row)
        except jsonschema.exceptions.ValidationError:
            # If validation fails, add the data to the failed table
            failed_table.put_item(Item=row)
