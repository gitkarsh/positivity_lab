import json
import csv

'''this file will change the data.json file
we are going to compute scores'''

locations = {}
with open("locations_classified.tsv", encoding="utf-8") as csvfile:
    readCSV = csv.reader(csvfile, delimiter='\t')
    for row in readCSV:
        line = list(row)
        latitude = line[0]
        longitude = line[1]
        if (latitude, longitude) not in locations:
            locations[latitude, longitude] = [0, 0]
        locations[latitude, longitude][0] += 1

with open("locations_classified.tsv", encoding="utf-8") as csvfile:
    readCSV = csv.reader(csvfile, delimiter='\t')
    for row in readCSV:
        line = list(row)
        latitude = line[0]
        longitude = line[1]
        catt = line[2]
        if catt == "positive":
            locations[latitude, longitude][1] += 1
        elif catt == "negative":
            locations[latitude, longitude][1] -= 1
figured = []
for i in locations:

    locations[i][1] = ((locations[i][1]/locations[i][0])+1)/2
    tag = list(i)
    tag.append(locations[i][1])
    figured.append(tag)

# Had to add "var data =" in order to get json file to read,
data = []
for i in figured:

    i[0] = round(float(i[0])+0.05/2, 2)
    i[1] = round(float(i[1])+0.05/2, 2)
    data.append({'score': round(i[2], 2), 'g': i[1], 't': i[0]})

with open('./public_html/data.js', 'w') as outfile:
    json.dump(data, outfile)

