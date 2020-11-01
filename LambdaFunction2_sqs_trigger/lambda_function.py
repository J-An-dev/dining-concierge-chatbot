import boto3
from boto3.dynamodb.conditions import Key
import json
import random
import pymysql


def lambda_handler(event, context):
    # Auth
    ACCESS_KEY = ''
    SECRET_KEY = ''
    REGION = ''

    # SQS message will be automatically pulled and passed through event
    queue_body = event['Records'][0]['body']

    content = json.loads(queue_body)
    phone = '+1' + content['PhoneNumber']
    time = content['DiningTime']
    date = content['DiningDate']
    people = content['NumberofPeople']
    cuisine = content["Cuisine"]
    region = content["Location"]

    # RDS
    conn = pymysql.connect(
        host="",
        user="",
        password="",
        cursorclass=pymysql.cursors.DictCursor
    )

    sql = 'select restaurant_id from `yelp-restaurants`.restaurant_info_clean where cuisine_type=%s and manhattan_region=%s'

    cur = conn.cursor()
    res = cur.execute(sql, (cuisine, region))
    rds_res = cur.fetchall()
    cur.close()

    id_all = []
    for i in range(len(rds_res)):
        id_all.append(list(rds_res[i].values())[0])

    suggestions_num = 3
    ids = []
    for i in range(suggestions_num):
        id = id_all[random.randint(0, len(id_all) - 1)]
        if ids == []:
            ids.append(id)
        elif id != ids[i - 1]:
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
            Message += f"{i + 1}. {name}, located at {address} with the average rating of {rating} among {reviews} reviews given the price {price}.\n"
    Message += "\nEnjoy your meal!"

    # SNS
    sns = boto3.client('sns', aws_access_key_id=ACCESS_KEY,
                       aws_secret_access_key=SECRET_KEY, region_name=REGION)
    sns.publish(
        PhoneNumber=phone, Message=Message
    )
    print(Message)

    return {
        'statusCode': 200,
    }

# lambda_handler(event=None, context=None)