import json
import pytest


@pytest.fixture
def create_activity_event():
    event_data = "events/create_activity_event.json"
    with open(event_data, "r") as f:
        return json.load(f)


def test_create_activity_201(create_activity_event, dynamodb_table, mocker):
    with mocker.patch("activities.connection.get_table", return_value=dynamodb_table):
        from activities import create_activity
        response = create_activity.lambda_handler(create_activity_event, "")

    payload = {
        "statusCode": 201,
        "headers": {},
        "body": json.dumps({"msg": "Activity created"}),
    }

    item = dynamodb_table.scan()

    assert item != ""
    assert create_activity_event["httpMethod"] == "POST"
    assert response == payload


def test_create_activity_400(dynamodb_table, mocker):
    with mocker.patch("activities.connection.get_table", return_value=dynamodb_table):
        from activities import create_activity
        response = create_activity.lambda_handler({}, "")

    payload = {
        "statusCode": 400,
        "headers": {},
        "body": json.dumps({"msg": "Bad Request"}),
    }

    assert response == payload
