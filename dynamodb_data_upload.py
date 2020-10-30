import boto3
import csv
from datetime import datetime

dynamodb = boto3.resource('dynamodb',region_name='region_name',aws_access_key_id="aws_access_key_id", aws_secret_access_key="aws_secret_access_key",verify=False)
table = dynamodb.Table('yelp-restaurants')
print(table.creation_date_time)

with open("restaurant_info_clean.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    data = []
    for row in reader:
        data.append(row)

    for r in range(1, len(data)):
        restaurant_id = data[r][0]
        restaurant_name = data[r][1]
        cuisine_type = data[r][2]
        restaurant_address = data[r][3]
        zip_code = restaurant_address.split("'")[-2].split()[-1]
        latitude = data[r][4]
        longitude = data[r][5]
        manhattan_region = data[r][6]
        restaurant_rating = data[r][7]
        review_count = data[r][8]
        price = data[r][9]
        insertedAtTimestamp = str(datetime.now())
        dynamo_info = {"BusinessID": restaurant_id, "Name": restaurant_name,
                       "CuisineType": cuisine_type, "Address": restaurant_address,
                       "ZipCode": zip_code,
                       "Latitude": latitude, "Longitude": longitude,
                       "ManhattanRegion": manhattan_region,
                       "Rating": restaurant_rating, "NumberofReviews": review_count,
                       "Price": price,
                       "InsertedAtTimestamp": insertedAtTimestamp}

        # dynamo_dict = {key: value for key, value in dynamo_info.items() if value}
        # print(dynamo_dict)

        insert = table.put_item(Item=dynamo_info)