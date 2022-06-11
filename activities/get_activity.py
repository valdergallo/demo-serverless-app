import json
from boto3.dynamodb.conditions import Key
from .connection import get_table


def lambda_handler(message, context):

    if "pathParameters" not in message or message["httpMethod"] != "GET":
        return {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({"msg": "Bad Request"}),
        }

    table = get_table()
    activity_id = message["pathParameters"]["id"]

    response = table.query(KeyConditionExpression=Key("id").eq(activity_id))

    return {"statusCode": 200, "headers": {}, "body": json.dumps(response)}
