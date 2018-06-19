import boto3
import json

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
    
    get_users()
    
    client = boto3.client('lambda')
    response = client.invoke(
    FunctionName='SAMEmailUsersAPI',
    InvocationType='RequestResponse',
    LogType='None',
#    Payload=json.dumps({"pathParameters":{"email":"test1@gmail.com"}})
)  
    data = clean(response)
    print('data: '+str(data))
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
 #   print ('jdattype: '+jdattype)
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
    for u in users:
        print ('users: '+str(u))

    if len(users) != 1:
        return False
    else:
        return True
    
    
def test_suite():
    
    test_data = []
#   Dyanmodb test
    dynamo_result = dynamoTest()
    print('dynamo test: '+str(dynamo_result))
  #  test_data.append(dynamo_result)
    
#   add a user    
    add_valid_return = add_user_valid_paramaters()
    test_data.append(add_valid_return)
    print('add user valid parameters: '+str(add_valid_return))
    
    #get users test
    user_result = get_users_test()
    test_data.append(user_result)
    
    #email test
    email_response = email_users_test()
    test_data.append(email_response)
    
    delete_users_return = delete_users_valid_paramaters()
    test_data.append(delete_users_return)
 #   print('delete user valid paramets: ' +str(delete_users_return))    


    for test in test_data:
        if test == True:
            print ('Pass')
        else:
            return False
            
        return True
        
            

def lambda_handler(event, context):
    response = test_suite()
    return response
    


    
    
    
