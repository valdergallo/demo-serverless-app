import json
import pytest


@pytest.fixture
def delete_activity_event():
    event_data = "events/delete_activity_event.json"
    with open(event_data, "r") as f:
        return json.load(f)


def test_update_activity_200(dynamodb_table, delete_activity_event):
    from activities import delete_activity

    response = delete_activity.lambda_handler(delete_activity_event, "")

    payload = {"msg": "Activity deleted"}

    data = json.loads(response["body"])

    response = dynamodb_table.scan()

    assert delete_activity_event["httpMethod"] == "DELETE"
    assert data == payload
    assert response["Items"] == []


def test_update_activity_400(dynamodb_table):
    from activities import delete_activity

    response = delete_activity.lambda_handler({}, "")

    payload = {
        "statusCode": 400,
        "headers": {},
        "body": json.dumps({"msg": "Bad Request"}),
    }

    assert response == payload
