from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from decimal import *
from boto3.dynamodb.conditions import Key, Attr

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def symptoms_get(event):
    result = "You may be safe"
    # TODO implement
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    table = dynamodb.Table('csymptoms')
    response = table.scan()

    symptoms = None
    symptom = event["body-json"].get('symptoms',None)
    if symptom:
        symptoms = symptom.split(',')
        
    
    medicalIssues = event["body-json"].get('medicalIssues',None)
    badHabits = event["body-json"].get('badHabits',None)
    #print(json.dumps(context))
    print("Covid19 testing centers")
    items = response["Items"]
    r_flag = False
    a = Decimal('1')
    m_flag = False
    for item in items:
        if r_flag == True:
            break
        m_flag=False
        print(item)
        result = "You may be safe"
        for s in symptoms:
            print(s)
            
            if s.upper() in item["symptoms"].upper() :
                print(s,"symptom is found in ",item["symptoms"])
                b=item['severity']
                print(item["severity"])
                result =  item["result"]
                if b.compare(a)==0:
                    result =  item["result"]
                    print("start")
                    r_flag = True
                    break
                else:
                    if medicalIssues.upper() in item.get("medicalIssues",'').upper() :
                        if badHabits.upper() in item.get("badHabits",'').upper():
                            result =  item["result"]
                            print("end")
            
                            m_flag = True
                            r_flag = True
                            break
                        else:
                            result =  item["result"]
                    

                            
            
                        
                
            if r_flag == True or m_flag==True:
                break
            
            
        if r_flag == True:
            break
        
    if r_flag == False and "No".upper()==symptom.upper():
        for item in items:
            if item.get("symptoms")=="No" and medicalIssues.upper() in item.get("medicalIssues",'').upper() :
                if badHabits.upper() in item.get("badHabits",'').upper():
                    result =  item["result"]
                    print("end")
    
                    r_flag = True
                    break
                else:
                    result =  item["result"]
            if r_flag == True:
                break
            
    #print(result)
    #'body': json.dumps(response)
    return {
        'statusCode': 200,
        'body':(result)
    }
def centers_get(state):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    table = dynamodb.Table('covid19')
    #print(json.dumps(context))
    print("Covid19 testing centers")
    
    response = table.query(
        KeyConditionExpression=Key('state').eq(state)
    )
    #response = response["body-json"]
    print(response)
    #'body': json.dumps(response)
    return {
        'statusCode': 200,
        'body':response["Items"]
    }
def lambda_handler(event, context):
    # TODO implement

    print(event)
    state = event["body-json"].get('state',None)
    
    if state == None:
        return symptoms_get(event)
    else:
        return centers_get(state)
