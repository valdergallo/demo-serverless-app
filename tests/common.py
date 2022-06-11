import boto3
import json
import os
import pytest
from moto import mock_dynamodb2
from unittest.mock import patch
from activities.create_activity import lambda_handler
from contextlib import contextmanager
from activities.constants import TABLE_NAME


def dynamodb_conn():
    with mock_dynamodb2():
        conn = set_up_dynamodb()
        return conn


def set_up_dynamodb():
    conn = boto3.resource(
        "dynamodb",
        region_name="us-east-1",
        aws_access_key_id="mock",
        aws_secret_access_key="mock",
    )
    conn.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {"AttributeName": "id", "KeyType": "HASH"},
            {"AttributeName": "date", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "id", "AttributeType": "S"},
            {"AttributeName": "date", "AttributeType": "S"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    )
    return conn
