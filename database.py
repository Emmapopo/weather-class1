import pickledb


class Database():
    def __init__(self):
        self.db = pickledb.load('history.db', False)
        self.db.dump()

    def Save(self, key, value):
        response = False
        if key not in self.db.getall():
            response = self.db.set(key, {value["timestamp"]:value["data"]})
        else:
            response = self.db.dadd(key, (value["timestamp"],value["data"]))
        self.db.dump()
        return response

    def Show(self, key):
        try:
            response = self.db.dgetall(key)
            f
        except:
            response = False
        return response
