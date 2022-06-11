import json
import pytest
from activities.constants import TABLE_NAME

PAYLOAD = {
    "id": "#123#123#",
    "date": "9999999999.999999",
    "stage": "BACKLOG",
    "description": "New Activity",
}


@pytest.fixture
def put_item_dynamodb(dynamodb_table):
    dynamodb_table.put_item(TableName=TABLE_NAME, Item=PAYLOAD)


@pytest.fixture
def get_activity_event():
    event_data = "events/get_activity_event.json"
    with open(event_data, "r") as f:
        return json.load(f)


def test_get_activity_200(get_activity_event, put_item_dynamodb, dynamodb_table):
    from activities import get_activity

    response = get_activity.lambda_handler(get_activity_event, "")
    data = json.loads(response["body"])
    assert get_activity_event["httpMethod"] == "GET"
    assert data["Items"][0] == PAYLOAD


def test_get_activity_400(dynamodb_table):
    from activities import get_activity

    response = get_activity.lambda_handler({}, "")

    payload = {
        "statusCode": 400,
        "headers": {},
        "body": json.dumps({"msg": "Bad Request"}),
    }

    assert response == payload
