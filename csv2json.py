import csv
import json

with open("restaurant_info_clean.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    data = []
    for row in reader:
        data.append(row)

    for r in range(1, len(data)):
        restaurant_id = data[r][0]
        cuisine_type = data[r][2]
        manhattan_region = data[r][6]
        l1 = {"index": {"_index": "restaurants", "_id" : r, "_type": "Restaurant"}}
        l1 = json.dumps(l1)
        l2 = {"RestaurantID": restaurant_id, "Cuisine": cuisine_type, "Region": manhattan_region}
        l2 = json.dumps(l2)

        with open("restaurant_info_clean.json", "a") as outfile:
            outfile.write(l1)
            outfile.write("\n")
            outfile.write(l2)
            outfile.write("\n")
