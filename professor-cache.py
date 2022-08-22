import time
import json
import boto3
from decimal import Decimal
expdate = int( time.time() ) + 86400

client = boto3.client('lambda')
dynamodb = boto3.resource('dynamodb')


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

def lambda_handler(event, context):

    cached_professor = dynamodb.Table('professors')

    response = cached_professor.get_item(
        Key={
            'professorFirst' : event['pathParameters']['professorFirst'].capitalize(),
            'professorLast' : event['pathParameters']['professorLast'].capitalize()
        }
    )
    if 'Item' in response:
        return {
            "statusCode": 200,
            "body": json.dumps(response['Item'],cls=DecimalEncoder),
            "isBase64Encoded": "false",
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": '*'
            }
        }
    else:
        inputParams = {
            'name' : event['pathParameters']['professorFirst'] + '. ' + event['pathParameters']['professorLast'] + '.',
            'site': 'Pomona',
            'expdate' : expdate
        }

        response = client.invoke(
            FunctionName = 'arn:aws:lambda:us-west-1:606504888305:function:rmp-scraper',
            InvocationType = 'RequestResponse',
            Payload = json.dumps(inputParams)
        )

        body = json.dumps(json.load(response['Payload']))
        cached_data = json.loads(body, parse_float=Decimal)
        cached_professor.put_item(Item=cached_data)

        return {
            "statusCode": 200,
            "body": body,
            "isBase64Encoded": "false",
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": '*'
            }
        }
        
