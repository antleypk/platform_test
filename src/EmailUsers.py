import boto3
import os
import json
from botocore.exceptions import ClientError
from botocore.vendored import requests


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
    BODY_TEXT = ("Ron Swanson Quotes for all"
                )
            
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>Ron Swanson Quotes</h1>
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



def get_message():
    response = requests.get("https://ron-swanson-quotes.herokuapp.com/v2/quotes")
    #print str(response.text)
    message = response.text
    
    message_one = ''
    quote =''
    for i in range(1,len(message)):
        message_one = message_one + str(message[i])
    trim_var = len(message)-2
    for b in range(0,trim_var):
        quote = quote + message_one[b]
    print ('quote: '+quote )   
    return quote
    
def get_users():
    users  = []
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['Users'])
    table_results = table.scan()
    x = table_results
    items = x['Items']
    for i in items:
        email = i['email']
        print ('email at 119: '+str(email))
        users.append(email)
    print ('completed scan')
    return users


def email_machine(users, message):
    for u in users:
        fra = []
        fra.append(message)
        fra.append(str(u))
        send(fra)

 
    

def lambda_handler(event, context):
    message = get_message()
    users = get_users()
    email_machine(users, message)
    
    data = {'exit_code': '0',
        'message': 'emails sent' }
    
    response = {
        "statusCode": 200,
        "body": json.dumps(data)
        }
    return response



