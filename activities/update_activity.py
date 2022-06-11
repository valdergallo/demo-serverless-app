import json

from activities.connection import get_table


def lambda_handler(message, context):

    if "body" not in message or message["httpMethod"] != "PUT":
        return {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({"msg": "Bad Request"}),
        }

    table = get_table()
    activity = json.loads(message["body"])

    params = {"id": activity["id"], "date": activity["date"]}

    table.update_item(
        Key=params,
        UpdateExpression="set stage = :s, description = :d",
        ExpressionAttributeValues={
            ":s": activity["stage"],
            ":d": activity["description"],
        },
        ReturnValues="UPDATED_NEW",
    )

    return {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps({"msg": "Activity updated"}),
    }
