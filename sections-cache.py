import json
import boto3
import time
from boto3.dynamodb.conditions import Key, Attr

client = boto3.client('lambda')
dynamo = boto3.resource('dynamodb')
expdate = int( time.time() ) + 86400

def lambda_handler(event, context):
    print(event['pathParameters'])
    print(context)

    cached_sections = dynamo.Table('sections')

    response = cached_sections.query(
        KeyConditionExpression=
            Key('term').eq(event['pathParameters']['term']) &
            Key('subject').eq(event['pathParameters']['subject']),
        FilterExpression=Attr('catalogNumber').eq(event['pathParameters']['catalogNumber'])
    )

    if response['Items']:
        return {
            "statusCode": 200,
            "body": json.dumps(response['Items'])['classes'],
            "isBase64Encoded": "false",
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": '*'
            }
        }
    else:

        inputParams = {
            "term"    : event['pathParameters']['term'],
            "subject" : event['pathParameters']['subject'],
            "number"  : event['pathParameters']['catalogNumber']
        }

        response = client.invoke(
            FunctionName = 'arn:aws:lambda:us-west-1:606504888305:function:cpp-schedule-scraper',
            InvocationType = 'RequestResponse',
            Payload = json.dumps(inputParams)
        )

        body = json.dumps(json.load(response['Payload']))
        cached_data = {}
        cached_data['term'] = event['pathParameters']['term']
        cached_data['subject'] = event['pathParameters']['subject']
        cached_data['number'] = event['pathParameters']['catalogNumber']
        cached_data['classes'] = json.loads(body)
        cached_data['expdate'] = expdate

        cached_sections.put_item(Item=cached_data)

        return {
            "statusCode": 200,
            "body": body,
            "isBase64Encoded": "false",
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": '*'
            }
        }
