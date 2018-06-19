import boto3
import os
import json
from botocore.exceptions import ClientError
from botocore.vendored import requests


def add_user_valid_paramaters():
    client = boto3.client('lambda')
    
    response = client.invoke(
    FunctionName='SAMAddUser',
    InvocationType='RequestResponse',
    LogType='None',
    Payload=json.dumps({"pathParameters":{"email":"test1@gmail.com"}})
)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
    data = clean(response)
    ec = data['exit_code']
    
    if str(ec) == '0':
        return True
    else:
        return False
 
def get_users():
    client = boto3.client('lambda')
    response = client.invoke(
    FunctionName='SAMGetUsers',
    InvocationType='RequestResponse',
    LogType='None',
)              
    data = clean(response)
    emails = data['Items']
    return emails


def email_users_test():
    client = boto3.client('lambda')
    response = client.invoke(
    FunctionName='SAMEmailUsersAPI',
    InvocationType='RequestResponse',
    LogType='None',
)  
    data = clean(response)
    exit_code = data['exit_code']
    if exit_code =='0':
        return True
    else:
        return False
    

def delete_users_valid_paramaters():
    client = boto3.client('lambda')
    
    response = client.invoke(
    FunctionName='SAMDeleteUser',
    InvocationType='RequestResponse',
    LogType='None',
    Payload=json.dumps({"pathParameters":{"email":"test1@gmail.com"}})
)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
    data = clean(response)
    
    if str(data) == 'test1@gmail.com':
        return True
    else:
        return False

    return False
    
def clean(response):
    data = response['Payload'].read()
    datatype = str(type(data))
#    print ('datatype: '+datatype)
    ddata = data.decode("utf-8") 
#    print ('ddate: '+str(ddata))
    jdat = json.loads(ddata)
    jdattype = str(type(jdat))
#    print ('jdattype: '+jdattype)
#    print ('jdat: '+str(jdat))
    jdatbody = jdat['body']
 #   print ('jdatbody: '+ str(jdatbody))
    body = json.loads(jdatbody)
    dat = body
    return dat

def dynamoTest():
    results = []
    users = get_users()
    
    results.append(users)
    if len(users)==0:
        return True
    else:
        return False



def get_users_test():
    users = get_users()
    check = False

    for u in users:
        if u['email'] == 'test1@gmail.com':
            check = True
    return check
    
    
def test_suite():
    
    test_data = []
    #Dyanmodb test
    dynamo_result = dynamoTest()
    print('dynamo test: '+str(dynamo_result))
    test_data.append(dynamo_result)
    
    #add a user    
    add_valid_return = add_user_valid_paramaters()
    test_data.append(add_valid_return)
    print('add user: '+str(add_valid_return))
    
    #get users test
    user_result = get_users_test()
    print ('Get Users Test: '+str(user_result))
    test_data.append(user_result)
    
    #email test
    email_response = email_users_test()
    test_data.append(email_response)
    print('email test: ' + str(email_response))
    
    delete_users_return = delete_users_valid_paramaters()
    test_data.append(delete_users_return)
    print('delete user test: ' +str(delete_users_return))    

    check = 'True'
    for test in test_data:
        if str(test) == 'False':
            check = 'False'
            notify()
        
    return check 
       

            
def notify():
    print('notify dev team')
    
    message = 'Unit tests suggest a resource is failing; notify the developer'    
    recipient = 'peterantley@gmail.com'
    frame = []
    frame.append(message)
    frame.append(recipient)
    
def send(frame):
    message = frame[0]
    recipient = frame[1]
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "peterantley@gmail.com"

    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    #RECIPIENT = "amskhan@gmail.com"
    RECIPIENT = recipient

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the 
 #   ConfigurationSetName=CONFIGURATION_SET # argument below.
    CONFIGURATION_SET = "Configset"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"

    # The subject line for the email.
    SUBJECT = message

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Unit Test Failed for SAM Project"
                )
            
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>Unit Test Failed</h1>
    This email was sent with AWS SES for a serverless solution provided by antleypk

    </body>
    </html>
                """            

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
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
            # If you are not using a configuration set, comment or delete the
            # following line
            ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])



def lambda_handler(event, context):
    response = test_suite()
    return response
    


    
    
    
