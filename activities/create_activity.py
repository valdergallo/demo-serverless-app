import json
import uuid
from datetime import datetime

from activities.connection import get_table
from activities.constants import TABLE_NAME


def lambda_handler(message, context):

    if "body" not in message or message["httpMethod"] != "POST":
        return {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({"msg": "Bad Request"}),
        }

    table = get_table()
    activity = json.loads(message["body"])

    params = {
        "id": str(uuid.uuid4()),
        "date": str(datetime.timestamp(datetime.now())),
        "stage": activity["stage"],
        "description": activity["description"],
    }

    table.put_item(TableName=TABLE_NAME, Item=params)

    return {
        "statusCode": 201,
        "headers": {},
        "body": json.dumps({"msg": "Activity created"}),
    }
