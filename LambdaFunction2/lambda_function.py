from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
from boto3.dynamodb.conditions import Key
import json
import random


def lambda_handler():
    # Auth
    ACCESS_KEY = 'ACCESS_KEY'
    SECRET_KEY = 'SECRET_KEY'
    REGION = 'REGION'
    awsauth = AWS4Auth(ACCESS_KEY, SECRET_KEY, REGION, 'es')

    # SQS
    sqs = boto3.client('sqs', aws_access_key_id=ACCESS_KEY,
                       aws_secret_access_key=SECRET_KEY, region_name=REGION)
    queue = sqs.get_queue_url(QueueName='Q1')
    queue_info = sqs.receive_message(QueueUrl=queue['QueueUrl'])
    # print(json.dumps(queue_info, indent=2))
    content = queue_info.get('Messages', None)
    if not content:
        return {
            'statusCode': 404,
        }
    content = queue_info['Messages'][0]['Body']
    # handle = queue_info['Messages'][0]['ReceiptHandle']
    # print(handle)
    content = json.loads(content)
    phone = '+1' + content['PhoneNumber']
    time = content['DiningTime']
    date = content['DiningDate']
    people = content['NumberofPeople']
    cuisine = content["Cuisine"]
    region =  content["Location"]
    # sqs.delete_message(
    #     QueueUrl=queue['QueueUrl'],
    #     ReceiptHandle=handle
    # )

    # Elasticsearch
    endpoint = 'search-chatbot-ruwuv46kgrvz2rmjihr3zxem3i.us-east-1.es.amazonaws.com'
    es = Elasticsearch(
        hosts=[{'host': endpoint, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    query_body = {
        "from": 0,
        "size": 450,
        "query": {
            "bool": {
                "filter": [
                    {
                        "bool": {
                            "must": [
                                {
                                    "bool": {
                                        "must": [
                                            {
                                                "term": {
                                                    "Cuisine.keyword": {
                                                        "value": cuisine,
                                                        "boost": 1
                                                    }
                                                }
                                            },
                                            {
                                                "term": {
                                                    "Region.keyword": {
                                                        "value": region,
                                                        "boost": 1
                                                    }
                                                }
                                            }
                                        ],
                                        "boost": 1
                                    }
                                }
                            ],
                            "boost": 1
                        }
                    }
                ],
                "boost": 1
            }
        },
        "_source": {
            "includes": [
                "RestaurantID"
            ],
            "excludes": []
        }
    }

    response = es.search(index="restaurants", body=query_body)['hits']['hits']
    id_all = [r['_source']['RestaurantID'] for r in response]

    suggestions_num = 3
    ids = []
    for i in range(suggestions_num):
        id = id_all[random.randint(0, len(id_all)-1)]
        if ids == []:
            ids.append(id)
        elif id != ids[i-1]:
            ids.append(id)

    # DynamoDB
    dynamodb = boto3.resource('dynamodb', aws_access_key_id=ACCESS_KEY,
                              aws_secret_access_key=SECRET_KEY, region_name=REGION)
    table = dynamodb.Table('yelp-restaurants')
    Message = f"Hey there! Here are my restaurant suggestions for {cuisine} cuisine in {region} for {people} people on {date} at {time}: \n\n"
    for i in range(len(ids)):
        response = table.query(KeyConditionExpression=Key('BusinessID').eq(ids[i]))['Items'][0]
        name = response['Name']
        address = response['Address'].split("'")[1]
        reviews = response['NumberofReviews']
        rating = response['Rating']
        price = response.get('Price', None)
        if not price:
            Message += f"{i + 1}. {name}, located at {address} with the average rating of {rating} among {reviews} reviews.\n"
        else:
            Message += f"{i+1}. {name}, located at {address} with the average rating of {rating} among {reviews} reviews given the price {price}.\n"
    Message += "\nEnjoy your meal!"

    # SNS
    sns = boto3.client('sns', aws_access_key_id=ACCESS_KEY,
                       aws_secret_access_key=SECRET_KEY, region_name=REGION)
    sns.publish(
        PhoneNumber=phone, Message=Message
    )
    return {
        'statusCode': 200,
    }

# lambda_handler()