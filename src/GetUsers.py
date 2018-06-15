#--------------------------------------------------
# Get User 
#--------------------------------------------------
# Author   |  Date             |  Notes
#--------------------------------------------------
# antleypk | 14 - June - 2018  | Created
#--------------------------------------------------
#--------------------------------------------------



import boto3
import os
import json

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['Users'])
    table_results = table.scan()

    response = {
        "statusCode": 200,
        "body": json.dumps(table_results)
        }
    return response