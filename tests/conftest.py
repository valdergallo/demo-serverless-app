import os

import boto3
import pytest
from moto import mock_dynamodb2

from activities.constants import TABLE_NAME

GET_TABLE_PATH = "activities.connection.get_table"


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture(scope="function")
def dynamodb(aws_credentials):
    with mock_dynamodb2():
        yield boto3.resource("dynamodb", region_name="us-east-1")


@pytest.fixture(scope="function")
def dynamodb_table(dynamodb, mocker):
    db_table = dynamodb.Table(TABLE_NAME)
    with mocker.patch(GET_TABLE_PATH, return_value=db_table):
        yield db_table


@pytest.fixture(scope="function", autouse=True)
def use_activities_db_moto(dynamodb):
    dynamodb.create_table(
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
    yield
