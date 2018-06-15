#--------------------------------------------------
# Add User 
#--------------------------------------------------
# Author   |  Date             |  Notes
#--------------------------------------------------
# antleypk | 14 - June - 2018  | Created
#--------------------------------------------------
#--------------------------------------------------

import boto3
import json
import os
import decimal

def add_to_users(email):
    print 'email: '+str(email)
    db_insert(email)
    success = 0
    data = {}
    data['exit_code'] = success
    data['email'] = email
    return data


def db_insert(email):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['Users'])
    
    response = table.put_item(
    Item={ 'email': email}
    )
    print ('response: '+str(response))

    
def lambda_handler(event, context):
    print 'context: ' + str(context)
    print 'event: ' + str(event)
    email = str(event['pathParameters']['email'])
    data = add_to_users(email)
    
    return {
        'statusCode': 200,
        'headers': { 'Content-Type': 'application/json' },
        'body': json.dumps(data)
    }
    

