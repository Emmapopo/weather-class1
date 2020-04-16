class WeatherModel():
    def __init__(self, location, timestamp = 0, temperature = 0, humidity = 0):
        self.location = location
        self.temperature = temperature
        self.humidity = humidity
        self.timestamp = timestamp

    def SetLocation(self, location):
        self.location = location
    
    def GetLocation(self):
        return self.location

    def SetTemperature(self, temperature):
        self.temperature = temperature
    
    def GetTemperature(self):
        return self.temperature
    
    def SetHumidity(self, humidity):
        self.humidity = humidity
    
    def GetHumidity(self):
        return self.humidity
    
    def SetTimestamp(self, timestamp):
        self.timestamp = timestamp
    
    def GetTimestamp(self):
        return self.timestamp

    def Save(self, db):
        previous = db.Get()
        if self.location not in previous:
            return self.save_new(db)
        else:
            return self.add_to_existing(db)

    def save_new(self, db):
        return db.Save(self.location, {self.timestamp:[self.temperature, self.humidity]})

    def add_to_existing(self, db):
        return db.Update(self.location, (self.timestamp,[self.temperature, self.humidity]))
