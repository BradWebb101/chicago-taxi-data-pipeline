import boto3
from botocore.exceptions import ClientError
import hashlib

def authenticate(access_key, secret_key):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('auth_table')
    try:
        response = table.get_item(Key={'access_key': access_key})
    except ClientError as e:
        return False
    else:
        item = response.get('Item')
        if item and hashlib.sha256(item['secret_key']) == secret_key:
            return True
        else:
            return False
