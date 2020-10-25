import requests
import json
import time
from datetime import datetime
from pytz import timezone

def test_limit(lat, lon):

    for i in range(5):
        for j in range(62):
            entry = eval(get_from_api(float(lat) + j/62, lon))
            if "daily" in entry:
                print("%.2d tem" % j)
            else:
                print("%.2d nao tem" % j)
        time.sleep(60)

def get_season(date, lat):
    day = int(date[2])
    month = int(date[1])
    lat = float(lat)

    if lat > 0:
        if month >= 3 and month <= 6:
            if month == 3 and day < 20:
                return "Winter"
            if month == 6 and day > 21:
                return "Summer"
            return "Spring"
        if month > 6 and month <= 9:
            if month == 9 and day > 21:
                return "Autumn"
            return "Summer"
        if month > 9 and month <= 12:
            if month == 12 and day > 21:
                return "Winter"
            return "Autumn"
        if month < 3:
            return "Winter"   
    else:
        if month >= 3 and month <= 6:
            if month == 3 and day < 20:
                return "Summer"
            if month == 6 and day > 21:
                return "Winter"
            return "Autumn"
        if month > 6 and month <= 9:
            if month == 9 and day > 21:
                return "Srping"
            return "Winter"
        if month > 9 and month <= 12:
            if month == 12 and day > 21:
                return "Summer"
            return "Spring"     
        if month < 3:
            return "Summer"


def get_from_api(lat, lon):
    api_key = "b3b03f6d1ec8887d0f0670c4be2ee2e7"

    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)

    request = requests.get(url) 

    return request.text

def get_from_text(file):
    f = open(file, "r")
    
    # do something
    json_data = json.load(f)

    text = "Precipitacao,Umidade,Nebulosidade,TempMaxima,TempMinima,DiaMes,Temp2,Temp4,Temp6,Vento,Periodo"
    

    for entry in json_data["daily"]:
        text += "\n"
        if "rain" in entry:
            text += str(entry["rain"]) + ","
        elif "snow" in entry:
            text += str(entry["snow"]) + ","
        else:
            text += str(entry["pop"] )+ ","

        text += str(entry["humidity"]) + ","
        text += str(entry["clouds"] / 10) + ","
        text += str(entry["temp"]["max"]) + ","
        text += str(entry["temp"]["min"]) + ","

        dt = datetime.fromtimestamp(entry["dt"], timezone('America/Sao_Paulo'))
        date = str(dt).split(" ")[0].split("-")
        text += date[2] + date[1] + ","
        
        text += str(entry["temp"]["morn"]) + "," + str(entry["temp"]["day"]) + "," + str(entry["temp"]["eve"]) + ","
        text += str(entry["wind_speed"]) + ","

        max = entry["temp"]["max"]
        min = entry["temp"]["min"]
        print("data: %s min: %.2f max: %.2f" % (dt, min, max))

    print(text)
    f.close()

def create_csv(file, lat, lon):
    request = get_from_api(lat, lon)

    # do something
    eval(request)
    json_data = json.loads(request)

    text = "Precipitacao,Umidade,Nebulosidade,TempMaxima,TempMinima,DiaMes,Temp2,Temp4,Temp6,Vento,Periodo"

    for entry in json_data["daily"]:
        text += "\n"
        if "rain" in entry:
            text += str(entry["rain"]) + ","
        elif "snow" in entry:
            text += str(entry["snow"]) + ","
        else:
            text += str(entry["pop"] )+ ","

        text += str(entry["humidity"]) + ","
        text += str(entry["clouds"] / 10) + ","
        text += str(entry["temp"]["max"]) + ","
        text += str(entry["temp"]["min"]) + ","

        dt = datetime.fromtimestamp(entry["dt"], timezone('America/Sao_Paulo'))
        date = str(dt).split(" ")[0].split("-")
        text += date[2] + date[1] + ","
        
        text += str(entry["temp"]["morn"]) + "," + str(entry["temp"]["day"]) + "," + str(entry["temp"]["eve"]) + ","
        text += str(entry["wind_speed"]) + ","
        text += get_season(date, lat)

    create_file(file, text)

def create_file(file, data):
    f = open(file, "w")
    f.write(data)
    f.close()

def main():      
    lat = "-29.68290769"
    lon = "-53.80132556"
    
    #request = get_from_api(lat, lon)
    #create_file("file.txt", request.text)

    #get_from_text("file.txt")
    create_csv("file.csv", lat, lon)
    #test_limit(lat, lon)

if __name__ == "__main__":
    main()