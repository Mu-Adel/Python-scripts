import requests
import pandas as pd
from API import API_KEY
import os



BASE_URL = "http://api.openweathermap.org/data/2.5"

def get_choice():
    choice = ""
    q = ""
    while choice not in ["0","1"] :
        choice = input("Would you like to get current weather status (0) or 5 day / 3 hour forecast (1). Enter(0/1) : ")
    return choice

def get_city():
    city = input("PLease enter city name : ").capitalize()
    return city

def get_current_weather(city):
    r = requests.get(f"{BASE_URL}/weather?q={city}&appid={API_KEY}&units=metric")
    if r.status_code == 200:
        json_dict = r.json()

        print('-' * 40)
        print(f"Displaying weather status for {city}, {json_dict['sys']['country']} ... ")
        print('-' * 40)

        print(f"The weather in {city} now is : ", json_dict['weather'][0]['main'])
        print(f"The temperature in {city} now is : ", json_dict['main']['temp'], "°C")
        print(f"The humidity in {city} now is : ", json_dict['main']['humidity'], "%")
        print('-' * 40)

    else:
        print("City  is not correct :(")
        main()


def get_weather_forcecast(city):
    r = requests.get(f"{BASE_URL}/forecast?q={city}&appid={API_KEY}&units=metric")

    if r.status_code == 200:
        json_dict = r.json()

        dict = {'city': json_dict['city']['name'],
                'country': json_dict['city']['country'],
                'dt':[],
                'temp':[],
                'temp_min': [],
                'temp_max': [],
                'humidity': [],
                'weather': [],
                'wind_speed': []}


        for i in json_dict['list']:
            dict['dt'].append(i['dt_txt'])
            dict['temp'].append(i['main']['temp'])
            dict['temp_min'].append(i['main']['temp_min'])
            dict['temp_max'].append(i['main']['temp_max'])
            dict['humidity'].append(i['main']['humidity'])
            dict['weather'].append(i['weather'][0]['main'])
            dict['wind_speed'].append(i['wind']['speed'])

        df = pd.DataFrame(dict)
        print('-' * 40)
        print(f"Displaying weather forecast for {city}, {json_dict['city']['country']} ... ")
        print('-' * 40)
        print(df)
        return df

    else:
        print("City  is not correct :(")
        main()


def main():
    while True:
        city_name = get_city()
        choice = get_choice()

        if choice == "0":
            get_current_weather(city_name)

        else:
            df = get_weather_forcecast(city_name)
            q = input("Would you like to save the forecasting data to Excel file? (Y/N) : ").upper()
            if q == 'Y':
                print("Generating file ... ")

                df.to_excel(f"{os.getcwd()}\{city_name}_weather.xlsx", index=False)


                print("Excel file has been generated :D")
            else:

                print(df)


if __name__ == "__main__":
    main()
