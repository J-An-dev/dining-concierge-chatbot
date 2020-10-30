import csv

with open("restaurant_info.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    restaurant_id = [row[0] for row in reader]
    id_set = set(restaurant_id)
    print(len(id_set))

with open("restaurant_info.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    data = []
    for row in reader:
        data.append(row)

    file = open("restaurant_info_clean.json", "a")
    writer = csv.writer(file)
    for i in range(len(data)):
        if data[i][0] in id_set:
            id_set.remove(data[i][0])
            writer.writerow(data[i])