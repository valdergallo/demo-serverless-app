import json
from .connection import get_table


def lambda_handler(message, context):

    if "httpMethod" not in message or message["httpMethod"] != "GET":
        return {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({"msg": "Bad Request"}),
        }

    table = get_table()

    response = table.scan()

    return {"statusCode": 200, "headers": {}, "body": json.dumps(response)}
