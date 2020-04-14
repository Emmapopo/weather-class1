# classes: history, current, forecast, parsing JSON,
import sys
import urllib.request, urllib.parse, urllib.error
import json
import ssl
import pickledb
import os

arguments =  str(sys.argv)
location = sys.argv[1][3:]
api_key = os.environ.get('api_key')
db = pickledb.load('history.db', False)

class Weather:
    def __init__(self):
        self.location = location
        self.api_key = api_key

    def current(self):
        self.serviceurl = 'http://api.openweathermap.org/data/2.5/weather?'
        self.url = self.serviceurl + 'q=' + self.location + '&APPID=' + self.api_key
        print('Retrieveing', self.url)
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
        print('Weather forecast for:', self.location)
        print('At', self.location, 'at time', self.time_stamp , 'the temperature is:', self.temp, 'while the humidity is', self.hum)
        self.dict = {str(self.time_stamp):self.dict_data}

        if location not in db.getall():
            db.set(self.dict_key, self.dict)
            db.dump()
        else:
            db.dadd(self.location,(str(self.time_stamp),self.dict_data))
            db.dump()

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
            print('At time:', self.time, ', temperature is:', self.temp, 'and humidity is:',self.hum)

    def history(self):
        self.log = db.dgetall(location)
        print('A history of weather data obtained from', self.location)
        for key in self.log:
            print('At time', key, 'the temperature and humidity are', self.log[key])

w1 = Weather()

if '-h' not in arguments and '-f' not in arguments :
    w1.current()
elif'-f' in arguments :
    w1.forecast()
else:
    w1.history()
