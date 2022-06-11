import boto3
from .constants import REGION, AWS_ENVIRONMENT, TABLE_NAME

_global_connection = None


def get_connection():
    global _global_connection

    if _global_connection:
        return _global_connection

    if AWS_ENVIRONMENT == "AWS_SAM_LOCAL":
        activities_table = boto3.resource(
            "dynamodb", endpoint_url="http://dynamodb:8000"
        )
    else:
        activities_table = boto3.resource("dynamodb", region_name=REGION)

    _global_connection = activities_table

    return _global_connection


def get_table(name_name=TABLE_NAME):
    activities_table = get_connection()
    return activities_table.Table(name_name)
