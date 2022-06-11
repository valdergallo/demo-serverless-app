import json
from unittest.mock import patch
from activities.create_activity import lambda_handler
from .common import dynamodb_conn

table_name = "Activities"

event_data = "events/create_activity_event.json"
with open(event_data, "r") as f:
    event = json.load(f)


@patch("activities.connection.get_connection", return_value=dynamodb_conn())
def test_create_activity_201(dynamodb_conn):
    response = lambda_handler(event, "")

    payload = {
        "statusCode": 201,
        "headers": {},
        "body": json.dumps({"msg": "Activity created"}),
    }

    item = dynamodb_conn.scan(TableName=table_name)

    assert item != ""
    assert event["httpMethod"] == "POST"
    assert response == payload


@patch("activities.connection.get_connection", return_value=dynamodb_conn())
def test_create_activity_400(dynamodb_conn):
    response = lambda_handler({}, "")

    payload = {
        "statusCode": 400,
        "headers": {},
        "body": json.dumps({"msg": "Bad Request"}),
    }

    assert response == payload
