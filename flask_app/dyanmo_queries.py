from main import client
from contextlib import contextmanager
import json
import os 
import boto3

def no_sql_get_all(limit) -> json:
    client = boto3.client('dynamodb')
    table_name = os.getenv('DYNAMO_TABLE_NAME')
   # query the table for the first 1000 rows
    response = client.scan(
        TableName=table_name,
        Limit=1000
    )

    # extract the items from the response
    items = response['Items']

    # continue scanning if there are more rows
    while 'LastEvaluatedKey' in response:
        response = client.scan(
            TableName=table_name,
            Limit=1000,
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        items.extend(response['Items'])

    return json.dumps(items['Items'])
