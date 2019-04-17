import os
import json
import boto3
from botocore.exceptions import ClientError


def notification(event, context):
    # TODO implement
    s3 = boto3.resource('s3')
    obj = s3.Object(event['Records'][0]['s3']['bucket']
                    ['name'], event['Records'][0]['s3']['object']['key'])
    res = obj.get()
    body = res['Body'].read()

    SENDER = os.environ['MAIL_SENDER']
    RECIPIENT = os.environ['MAIL_RECIPIENT']
    AWS_REGION = os.environ['SES_RESION']

    SUBJECT = "Posted in " + event['Records'][0]['s3']['object']['key']
    d = json.loads(body.decode('utf-8'))
    s = '\n'.join([f'{k}: {v}' for k, v in json.loads(d['body']).items()])
    BODY_TEXT = '# post data\n' + s + '\n\n# s3 contents dump\n' + \
        json.dumps(d, ensure_ascii=False) + \
        '\n\n# s3 event dump\n' + json.dumps(event)
    CHARSET = "UTF-8"

    client = boto3.client('ses', region_name=AWS_REGION)

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print(f"Email sent! Message ID:{response['MessageId']}")
