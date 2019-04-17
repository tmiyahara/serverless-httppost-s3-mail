import json
import datetime
import boto3
import os


def create(event, context):
    current_time = datetime.datetime.now().time()
    body = {
        "event": event,
        "time": str(current_time),
        "bucketname": os.environ['S3_POST_BUCKET'],
        "key": os.environ['S3_POST_KEY_BASE'] + '/' + event['requestContext']['requestId']
    }

    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"  # Required for CORS support to work
        },
        "body": json.dumps(body)
    }

    bucket_name = os.environ['S3_POST_BUCKET']
    key = os.environ['S3_POST_KEY_BASE'] + '/' + \
        event['requestContext']['requestId']
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket_name, key)

    obj.put(Body=bytearray(json.dumps(event), 'UTF-8'))

    return response
