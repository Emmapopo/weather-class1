import pickledb


class Database():
    def __init__(self):
        self.db = pickledb.load('history.db', False)
        self.db.dump()

    def Save(self, key, value):
        response = self.db.set(key, value)
        self.db.dump()
        return response

    def Update(self, key, value):
        response = self.db.dadd(key, value)
        self.db.dump()
        return response
    
    def Get(self):
        return self.db.getall()
        
    def GetKey(self, key):
        response = []
        try:
            response = self.db.dgetall(key)
        except:
            response = []
        return response
