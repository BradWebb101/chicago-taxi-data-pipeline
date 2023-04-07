import requests
import boto3
import os

def handler(event, context):
    # Set up S3 client
    s3_client = boto3.client('s3')

    # Set up request parameters
    url = 'https://data.cityofchicago.org/resource/wrvz-psew.json'
    #Please note i removed the header 'X-App-Token' as it reduced performance vs using a direct request
    headers = {}
    params = {}
    offset = 0

    # Stream data from API and save to S3
    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.content:
            filename = f'taxi_trips_out.json'
            with open(f'/tmp/{filename}', 'wb') as f:
                f.write(response.content)
                offset += 1000
                params['$offset'] = offset
                s3_client.upload_file(f'/tmp/{filename}', os.getenv('S3_DATA_LAKE_BUCKET'), filename)
        else:
            break

