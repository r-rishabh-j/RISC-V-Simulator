class Buffers:
    def __init__(self):
        self.RA = 0
        self.RZ = 0
        self.RM = 0
        self.RY = 0
        
    def getRA(self):
        return self.RA
    def getRZ(self):
        return self.RZ
    def getRM(self):
        return self.RM
    def getRY(self):
        return self.RY
        
    def setRA(self, val):
        self.RA = val
    def setRZ(self, val):
        self.RZ = val
    def setRM(self, val):
        self.RM = val
    def setRY(self, val):
        self.RY = val
