# classes: history, current, forecast, parsing JSON,
import sys
import urllib.request, urllib.parse, urllib.error
import json
import ssl
import pickledb
import os
import anotherOutput
from model import weather_model
from model import database

arguments =  str(sys.argv)
location = sys.argv[1][3:]
api_key = os.environ.get('api_key')
db = pickledb.load('history.db', False)

class Weather:
    def __init__(self, outputClass, databaseClass):
        self.location = location
        self.api_key = api_key
        self.output = outputClass
        self.database = databaseClass

    def current(self):
        self.serviceurl = 'http://api.openweathermap.org/data/2.5/weather?'
        self.url = self.serviceurl + 'q=' + self.location + '&APPID=' + self.api_key
        self.output.print('Retrieveing', self.url)
        self.uh = urllib.request.urlopen(self.url)
        self.data = self.uh.read().decode()
        try:
            self.js = json.loads(self.data)
        except:
            self.js = None
        X = self.js
        temp = X['main']['temp']
        hum = X['main']['humidity']
        time_stamp = X['dt']

        weather = weather_model.WeatherModel(self.location)
        weather.SetTemperature(temp)
        weather.SetHumidity(hum)
        weather.SetTimestamp(time_stamp)
        self.output.print('Weather forecast for:', weather.GetLocation())
        self.output.print('At', weather.GetLocation(), 'at time', weather.GetTimestamp() , 'the temperature is:', weather.GetTemperature(), 'while the humidity is', weather.GetHumidity())
        response = weather.Save(self.database)
        if not response:
            self.output.print("unable to save")

    def forecast(self):
        self.serviceurl = 'http://api.openweathermap.org/data/2.5/weather?'
        self.url = self.serviceurl + 'q=' + self.location + '&APPID=' + self.api_key
        self.uh = urllib.request.urlopen(self.url)
        self.data = self.uh.read().decode()
        try:
            self.js = json.loads(self.data)
        except:
            self.js = None

        X = self.js
        self.lon = X['coord']['lon']
        self.lon = str(self.lon)
        self.lat = X['coord']['lat']
        self.lat = str(self.lat)

        self.serviceurl1 = 'https://api.openweathermap.org/data/2.5/onecall?'
        self.url1 = self.serviceurl1 + 'lat=' + self.lat + '&lon=' + self.lon + '&appid=' + self.api_key
        self.uh1 = urllib.request.urlopen(self.url1)
        self.data1 = self.uh1.read().decode()
        try:
            self.js1 = json.loads(self.data1)
        except:
            self.js1 = None

        Y = self.js1
        self.start_time = Y['current']['dt']
        x = list(range(24))

        for a in x:
            self.time = Y['hourly'][a]['dt']
            self.temp = Y['hourly'][a]['temp']
            self.hum = Y['hourly'][a]['humidity']
            self.output.print('At time:', self.time, ', temperature is:', self.temp, 'and humidity is:',self.hum)

    def history(self):
        response = self.database.GetKey(self.location)
        print(response)
        self.output.print('A history of weather data obtained from', self.location)
        if not response:
            self.output.print("No history for", self.location)
            quit()
        for key in response:
            self.output.print('At time', key, 'the temperature and humidity are', response[key])




outputInstance = anotherOutput.Output()
databaseInstance = database.Database()

w1 = Weather(outputClass=outputInstance, databaseClass=databaseInstance)

if '-h' not in arguments and '-f' not in arguments :
    w1.current()
elif'-f' in arguments :
    w1.forecast()
else:
    w1.history()
