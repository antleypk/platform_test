import boto3
import json
import decimal
import os


def remove(email):
    print ('email to be remove: ' + email)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['Users'])
    
    response = table.delete_item(Key={'email':email})
    
    meta = response['ResponseMetadata']
    status = meta['HTTPStatusCode']
    
    print ('status: ' +str(status))
    
    print ('response: ' + str(response))
    
    return email 

def lambda_handler(event, context):
    # TODO implement
    email = str(event['pathParameters']['email'])
    remove(email)

    return {
        'statusCode': 200,
        'headers': { 'Content-Type': 'application/json' },
        'body': json.dumps(email)
    }
    

