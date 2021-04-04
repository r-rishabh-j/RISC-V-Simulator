#!/usr/bin/python3
# generates control signals for the ALU and muxes 
MAX_SIGNED_NUM=0x7fffffff
MIN_SIGNED_NUM=0x10000000
MAX_UNSIGNED_NUM=0xffffffff
MIN_UNSIGNED_NUM=0x00000000

class ControlModule:
	def __init__(self):
		self.opcode = 0
		self.funct3 = 0
		self.funct7 = 0
		self.rd = 0
		self.rs1 = 0
		self.rs2 = 0
		self.imm = 0

	def getOpcode(self):
		return self.opcode
	def getFunct3(self):
		return self.funct3
	def getFunct7(self):
		return self.funct7
	def getRd(self):
		return self.rd
	def getRs1(self):
		return self.rs1
	def getRs2(self):
		return self.rs2
	def getImm(self):
		return self.imm

	def setOpcode(self, opcode):
		self.opcode = opcode
	def setFunct3(self, funct3):
		self.funct3 = funct3
	def setFunct7(self, funct7):
		self.funct7 = funct7
	def setRd(self, rd):
		self.rd = rd
	def setRs1(self, rs1):
		self.rs1 = rs1
	def setRs2(self, rs2):
		self.rs2 = rs2
	def setImm(self, imm):
		self.imm = imm
	

circuit = ControlModule()


