import json
from .connection import get_table


def lambda_handler(message, context):

    if "pathParameters" not in message or message["httpMethod"] != "DELETE":
        return {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({"msg": "Bad Request"}),
        }

    table = get_table()
    activity_id = message["pathParameters"]["id"]
    activity_date = message["pathParameters"]["date"]

    params = {"id": activity_id, "date": activity_date}

    table.delete_item(Key=params)

    return {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps({"msg": "Activity deleted"}),
    }
