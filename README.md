<!--
title: 'AWS Simple HTTP Endpoint example in Python'
description:
framework: v1
platform: AWS
language: Python
authorLink: 'https://github.com/tmiyahara'
authorName: 'Tohiyuki Miyahara'
authorAvatar: ''
-->

# Serverless Framework サンプル

serveless framework のテンプレートです。任意のフォームでPOSTされた内容をS3のオブジェクトとして保存し、S3オブジェクト生成をトリガーに指定のメールアドレス宛てにメールを送信します。

## Setup

```bash
serverless install -u https://github.com/tmiyahara/serverless-httppost-s3-mail -n my-project
```

serverless.yml ファイルの以下の項目を設定ください

- custom.postform_id POSTされた内容を保存するバケット名の重複を避けるため
- custom.mail_recipient メール送信先(To)アドレスを指定します、事前にSESで受信可能なアドレスに設定が必要
- custom.mail_sender メール送信元(From)アドレスを指定します、事前にSESで送信可能なアドレスに設定が必要

## Deploy

```bash
serverless deploy
```

The expected result should be similar to:

```bash
Serverless: Packaging service...
Serverless: Uploading CloudFormation file to S3...
Serverless: Uploading service .zip file to S3 (758 B)...
Serverless: Updating Stack...
Serverless: Checking Stack update progress...
..........
Serverless: Stack update finished...

Service Information
service: aws-python-form-recieve-notification
stage: dev
region: us-east-1
stack: aws-python-form-recieve-notification-dev
resources: 16
api keys:
  None
endpoints:
  POST - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/contacts)
functions:
  create: form-recieve-notification-dev-create
  notification: form-recieve-notification-dev-notification
```

## Usage

curl コマンドを使って、endpointにHTTPリクエストします。

```bash
curl -X POST -H "Content-Type: application/json" -d '{"Name":"Taro Hiro", "Message":"hello"}' https://XXXXXXX.execute-api.us-east-1.amazonaws.com/dev/contacts
```

次のようなレスポンスが表示されます。また、設定したメールアドレスにメールが送信されています。

```bash
{
  "event": {
    "resource": "/contacts",
    "path": "/contacts",
    "httpMethod": "POST",
...
  },
  "time": "09:22:29.311113",
  "bucketname": "aws-python-form-recieve-notification-dev-xxxxxxx-records",
  "key": "dev/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

## Scaling

By default, AWS Lambda limits the total concurrent executions across all functions within a given region to 100. The default limit is a safety limit that protects you from costs due to potential runaway or recursive functions during initial development and testing. To increase this limit above the default, follow the steps in [To request a limit increase for concurrent executions](http://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html#increase-concurrent-executions-limit).
