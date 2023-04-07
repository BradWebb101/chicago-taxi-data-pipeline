import boto3
import json
import os
from moto import mock_s3, mock_dynamodb
import random

import sys
sys.path.clear()
sys.path.append('dynamo_put/')

# Initialize the DynamoDB client and resource
dynamodb = boto3.client('dynamodb')
dynamodb_resource = boto3.resource('dynamodb')

random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))

data_table_name = f'data_table_{random_string}'
failed_table_name = f'failed_table_{random_string}'
data_table = dynamodb_resource.create_table(
    TableName=data_table_name,
    KeySchema=[
        {
            'AttributeName': 'unique_key',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'unique_key',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)
failed_table = dynamodb_resource.create_table(
    TableName=failed_table_name,
    KeySchema=[
        {
            'AttributeName': 'unique_key',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'unique_key',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

@mock_s3
@mock_dynamodb
def test_lambda_handler():
    # Upload test data to S3
    s3 = boto3.resource('s3')
    bucket_name = 'test-bucket'
    bucket = s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
    'LocationConstraint': 'us-east-1'
})
    test_data = [{'unique_key': '123', 'taxi_id': 'abc', 'fare': '10.0'},
                 {'unique_key': '456', 'taxi_id': 'def', 'fare': '20.0'},
                 {'unique_key': '789', 'taxi_id': 'ghi', 'fare': '30.0'}]
    file_content = json.dumps(test_data)
    s3.Object(bucket_name, 'test.json').put(Body=file_content)

    # Define environment variables
    os.environ['PASSED_VALIDATION_TABLE'] = data_table_name
    os.environ['FAILED_VALIDATION_TABLE'] = failed_table_name

    from dynamo_put.main import handler
    event = {
        'Records': [
            {
                's3': {
                    'bucket': {
                        'name': bucket_name
                    },
                    'object': {
                        'key': 'test.json'
                    }
                }
            }
        ]
    }
    handler(event, {})

    # Check that the data was added to the data table
    response = data_table.get_item(Key={'unique_key': '123'})
    assert response['Item']['fare'] == 10.0
    response = data_table.get_item(Key={'unique_key': '456'})
    assert response['Item']['fare'] == 20.0
    response = data_table.get_item(Key={'unique_key': '789'})
    assert response['Item']['fare'] == 30.0

    # Check that the failed data was added to the failed table
    response = failed_table.get_item(Key={'unique_key': 'invalid'})
    assert 'Item' not in response
    response = failed_table.get_item(Key={'unique_key': 'invalid2'})
    assert 'Item' not in response
