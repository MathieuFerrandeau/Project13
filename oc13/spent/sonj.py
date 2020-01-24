import json
from django.db.utils import DataError, IntegrityError


with open('spent/json/init_db.json') as json_data:
    data = json.load(json_data)
    data1 = len(data["categories"]) - 1
    data2 =  data["categories"][1]["Scolarité & Enfants"][6]
    data3 = data["categories"][0]["Logement"][6]
    data4 = data["categories"][2]["Alimentation & Restau"][4]
    print(data1)
    #print(data1)
    #print(data4)
    i = 0
    while i <= data1:
        for category in data["categories"][i]:
            print(category)
            for test in data["categories"][i][category]:
                print(test + ' ' + category)
        i = i + 1





