# classes: history, current, forecast, parsing JSON,
import sys
import urllib.request, urllib.parse, urllib.error
import json
import ssl
import pickledb
import os
import anotherOutput
import database

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
        self.temp = X['main']['temp']
        self.hum = X['main']['humidity']
        self.time_stamp = X['dt']


        self.dict_key = self.location
        self.dict_data = [self.temp, self.hum]
        self.output.print('Weather forecast for:', self.location)
        self.output.print('At', self.location, 'at time', self.time_stamp , 'the temperature is:', self.temp, 'while the humidity is', self.hum)
        self.dict = {"timestamp": str(self.time_stamp), "data": self.dict_data}
        response = self.database.Save(self.dict_key, self.dict)
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
        self.log = db.dgetall(location)
        self.output.print('A history of weather data obtained from', self.location)
        for key in self.log:
            self.output.print('At time', key, 'the temperature and humidity are', self.log[key])

outputInstance = anotherOutput.Output()
databaseInstance = database.Database()
w1 = Weather(outputClass=outputInstance, databaseClass=databaseInstance)

if '-h' not in arguments and '-f' not in arguments :
    w1.current()
elif'-f' in arguments :
    w1.forecast()
else:
    w1.history()
