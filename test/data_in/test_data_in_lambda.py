import json
import os
import pytest
import boto3
from moto import mock_s3
import requests
import sys

import os

import sys
sys.path.append('data_in/')

# Import the lambda function handler
from main import handler

@pytest.fixture
def event():
    """Return a sample event."""
    return {
        "key": "value"
    }


@pytest.fixture
def context():
    """Return a sample context."""
    return {}


@pytest.fixture
def s3_client():
    """Mock the S3 client."""
    with mock_s3():
        client = boto3.client("s3", region_name="us-east-1")
        client.create_bucket(Bucket='moto_test_bucket')
        yield client


def test_handler(event, context, s3_client, monkeypatch):
    """Test the handler function."""
    # Create a mock response from the API
    data = [{"key": "value"}]
    response = requests.Response()
    response._content = json.dumps(data).encode("utf-8")

    # Mock the requests.get() function to return the mock response
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: response)

    # Call the handler function
    handler(event, context)

    # Check that the file was uploaded to S3
    objects = s3_client.list_objects_v2(Bucket='moto_test_bucket')
    assert len(objects["Contents"]) == 1
    assert objects["Contents"][0]["Key"] == "taxi_trips_out.json"
