import json
from botocore.vendored import requests
from urllib.parse import quote
import boto3
import logging


def lambda_handler(event, context):
    response = {"dialogAction": {
        "type": "Close",
        "fulfillmentState": "Fulfilled",
        "message": {
            "contentType": "PlainText",
            "content": "Message to convey to the user."
        }
    }
    }
    return dispatch(event)


def dispatch(event):
    intent = event['currentIntent']['name']
    logging.info(event)
    print('fef', event)

    if intent == "GreetingIntent":
        return {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": "Hi there! What can I do for you today?"
                }
            }
        }
    elif intent == "ThankYouIntent":
        return {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": "I'm glad I could be of help. Bye!"
                }
            }
        }
    elif intent == "DiningSuggestionsIntent":
        slot = event['currentIntent']['slots']
        location = slot['Location']
        foodtype = slot["Cuisine"]
        people = slot['NumberofPeople']
        date = slot['DiningDate']
        time = slot['DiningTime']
        phone = slot['PhoneNumber']

        sqs = boto3.resource('sqs', aws_access_key_id='aws_access_key_id',
                             aws_secret_access_key='aws_secret_access_key', region_name='region_name')
        queue = sqs.get_queue_by_name(QueueName='Preference')
        message = json.dumps(slot)

        response = queue.send_message(MessageBody=message)

        Messageshow = f"Alright, you're all set. Please let me repeat your preference: You'd like to have {foodtype} cuisine for {people} people in {location} on {date} at {time}. And your phone number is {phone}. Expect my suggestions shortly! Have a good day."

        return {"dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": Messageshow
            }
        }
        }
    else:
        return {"dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": "Sorry, it beyond my ability."
            }
        }
        }