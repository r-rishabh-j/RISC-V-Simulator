class Buffers:
    def __init__(self):
        self.R1 = 0
        self.R2 = 0
        self.R1temp = 0
        self.R2temp = 0
        self.RA = 0
        self.RB = 0
        self.RAtemp = 0
        self.RBtemp = 0
        self.RZ = 0
        self.RM = 0
        self.RMtemp = 0
        self.RY = 0
		self.Fetch_PC_temp = 0
		self.Decode_PC_temp = 0

    def getR1(self):
        return self.R1
    def getR2(self):
        return self.R2
    def getR1temp(self):
        return self.R1temp
    def getR2temp(self):
        return self.R2temp
    def getRA(self):
        return self.RA
    def getRB(self):
        return self.RB
    def getRAtemp(self):
        return self.RAtemp
    def getRBtemp(self):
        return self.RBtemp
    def getRZ(self):
        return self.RZ
    def getRM(self):
        return self.RM
    def getRMtemp(self):
        return self.RMtemp
    def getRY(self):
        return self.RY
	def getFetch_PC_temp(self):
		return self.Fetch_PC_temp
	def getDecode_PC_temp(self):
		return self.Decode_PC_temp

    def setR1(self, val, control_R1):
        if control_R1:
            self.R1 = val
    def setR2(self, val, control_R2):
        if control_R2:
            self.R1 = val
    def setR1temp(self, val, control_R1temp):
        if control_R1temp:
            self.R1 = val
    def setR2temp(self, val, control_R2temp):
        if control_R2temp:
            self.R1 = val
    def setRA(self, val, control_RA):
        if control_RA:
            self.R1 = val
    def setRB(self, val, control_RB):
        if control_RB:
            self.R1 = val
    def setRAtemp(self, val, control_RAtemp):
        if control_RAtemp:
            self.R1 = val
    def setRBtemp(self, val, control_RBtemp):
        if control_RBtemp:
            self.R1 = val
    def setRZ(self, val, control_RZ):
        if control_RZ:
            self.R1 = val
    def setRM(self, val, control_RM):
        if control_RM:
            self.R1 = val
    def setRMtemp(self, val, control_RMtemp):
        if control_RMtemp:
            self.R1 = val
    def setRY(self, val, control_RY):
        if control_RY:
            self.R1 = val
	def setFetch_PC_temp(self, val):
		self.Fetch_PC_temp = val
	def setDecode_PC_temp(self, val):
		self.Decode_PC_temp = val
