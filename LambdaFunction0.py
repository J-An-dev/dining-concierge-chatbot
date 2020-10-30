import json
import boto3

def lambda_handler(event, context):
    id_recieved = '2020'
    content_recieved = 'Hello'
    # print("Received event: " + json.dumps(event, indent=2))

    if len(event) > 0:
        content_recieved = event['messages'][0]['unstructured']['text']

    client = boto3.client('lex-runtime','region',aws_access_key_id="aws_access_key_id", aws_secret_access_key="aws_secret_access_key",verify=False)
    botresponse = client.post_text(
        botName='ChatBot',
        botAlias='Jarvis',
        userId=id_recieved,
        sessionAttributes={},
        requestAttributes={},
        inputText=content_recieved
    )

    response = {}
    response["text"] = botresponse["message"]
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }, 
        'messages': [ 
            {
                'type': "unstructured", 
                'unstructured': response
            }
        ]
    }
