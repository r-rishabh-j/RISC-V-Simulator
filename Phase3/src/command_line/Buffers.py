class Buffers:
    def __init__(self):
        self.RA = 0
        self.RB = 0
        self.RAtemp = 0
        self.RBtemp = 0
        self.RZ = 0
        self.RM = 0
        self.RMtemp = 0
        self.RY = 0
        self.RYtemp=0
        self.RZtemp=0
        self.IRbuffer=0 # to store output of fetch stage and used to update actual IR at the end of cycle
        self.Fetch_output_PC_temp = 0 # used to store the value of PC to be updated at the end of cycle
        self.Decode_output_PC_temp = 0 # used to store the correct value of PC at branch misprediction
        self.Decode_input_PC=0  # used to store the PC of the instruction in decode
        self.Decode_input_branch_prediction=False # used to store the branch prediction output for next cycle

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
            self.R2 = val
    def setR1temp(self, val, control_R1temp):
        if control_R1temp:
            self.R1temp = val
    def setR2temp(self, val, control_R2temp):
        if control_R2temp:
            self.R2temp = val
    def setRA(self, val, control_RA):
        if control_RA:
            self.RA = val
    def setRB(self, val, control_RB):
        if control_RB:
            self.RB = val
    def setRAtemp(self, val, control_RAtemp):
        if control_RAtemp:
            self.RAtemp = val
    def setRBtemp(self, val, control_RBtemp):
        if control_RBtemp:
            self.RBtemp = val
    def setRZ(self, val, control_RZ):
        if control_RZ:
            self.RZ = val
    def setRM(self, val, control_RM):
        if control_RM:
            self.RM = val
    def setRMtemp(self, val, control_RMtemp):
        if control_RMtemp:
            self.RMtemp = val
    def setRY(self, val, control_RY):
        if control_RY:
            self.RY = val
    def setFetch_output_PC_temp(self, val):
	    self.Fetch_output_PC_temp = val
    def setDecode_output_PC_temp(self, val):
        self.Decode_output_PC_temp = val

class Buffers_np:
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
