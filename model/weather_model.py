class WeatherModel(object):
    def __init__(self, location, temperature = 0, humidity = 0):
        self.location = location
        self.temperature = temperature
        self.humidity = humidity

    def Save(self, location, value):
        pass

    def save_new(self, location, new_dict):
        pass

    def add_to_existing(self, location, data):
        pass

    def GetLocationData():
        pass