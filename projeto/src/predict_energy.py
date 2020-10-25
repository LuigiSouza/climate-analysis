import pandas            as pd
import sys
import json
import io
import time
import requests
from sklearn.model_selection          import train_test_split
from sklearn.linear_model             import LinearRegression
from collections                      import OrderedDict
from datetime import datetime
from pytz import timezone


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

def create_csv(lat, lon):
    request = get_from_api(lat, lon)

    # do something
    eval(request)
    json_data = json.loads(request)

    text = "Precipitacao,Umidade,Nebulosidade,TempMaxima,TempMinima,DiaMes,Morn,Day,Eve,Vento,Periodo,Energia"

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

    return text

def create_file(file, data):
    f = open(file, "w")
    f.write(data)
    f.close()

# ==========================================================

def train_machinne(file_name):
    # loads the dataset
    arquivo = pd.read_csv(file_name)

    # split the data into training/testing sets
    y = arquivo['Energia']
    x = arquivo.drop('Energia', axis = 1)
    # drops the unecessary columns
    x = x.drop('Insolacao', axis = 1)
    x = x.drop('Data', axis = 1)
    x = x.drop('Estacao', axis = 1)            

    x['Periodo'] = x['Periodo'].replace('Winter', 1)
    x['Periodo'] = x['Periodo'].replace('Autumn', 2)
    x['Periodo'] = x['Periodo'].replace('Spring', 3)
    x['Periodo'] = x['Periodo'].replace('Summer', 4)

    # Split the targets into training/testing sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3)

    # Create linear regression object
    linear_model = LinearRegression()

    # Train the model using the training sets
    linear_model.fit(x_train, y_train)

    return linear_model

def predict_data(model, file_name):
    # loads the dataset used in real prediction
    if isinstance(file_name, str):
        x_hoje = pd.read_csv(file_name).drop('Energia', axis = 1)
    else:
        x_hoje = file_name.drop('Energia', axis=1)

    x_hoje['Periodo'] = x_hoje['Periodo'].replace('Winter', 1)
    x_hoje['Periodo'] = x_hoje['Periodo'].replace('Autumn', 2)
    x_hoje['Periodo'] = x_hoje['Periodo'].replace('Spring', 3)
    x_hoje['Periodo'] = x_hoje['Periodo'].replace('Summer', 4)

    # Make predictions using the testing set

    return model.predict(x_hoje)

def main():      
    #lat = sys.argv[1]
    #lon = sys.argv[2]
    lat = "-29.68290769"
    lon = "-53.80132556"
    data_training = "planilha_header.csv"
    
    data_extracted = create_csv(lat, lon)
    data_predict = pd.read_csv(io.StringIO(data_extracted))
    create_file("file2.csv", data_extracted)

    linear_model = train_machinne(data_training)
    print_result = predict_data(linear_model, data_predict)
    
    # starts the output file
    planilha = open("energia.csv", "w")

    for i in print_result:
        planilha.write(str(i) + "\n")
    
    planilha.close()    

    #request = get_from_api(lat, lon)
    #get_from_text("file.txt")


if __name__ == "__main__":
    main()