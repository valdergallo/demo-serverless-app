import json

def lambda_handler(message, context):
    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps({'msg': 'Hello World'})
    }
