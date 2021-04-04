#!/usr/bin/python3
# generates control signals for the ALU and muxes 
import math
#addi 19 0
#andi 19 7
#ori 19 6
#lb 3 0
#lh 3 1
#lw 3 2
#jalr 103 0
I = [19, 3, 103] #opcodes for I

#sb 35 0
#sh 35 1
#sw 35 2
S = [35] #opcode for S

#auipc 23
#lui 55
U = [23, 55]  #opcodes for U

#add 51 0 0
#and 51 7 0
#or 51 6 0
#sll 51 1 0
#slt 51 2 0
#sra 51 5 32
#srl 51 5 0
#sub 51 0 32
#xor 51 4 0
#mul 51 0 1
#div 51 4 1
#rem 51 6 1
R = [51]  #opcode for R
SB = [99]  #opcode for SB
UJ = [111] #opcode for UJ
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
        self.decoder=DecodeModule()

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

class DecodeModule:

    def __init__(self):
		self.opcode = 0
		self.funct3 = 0
		self.funct7 = 0
		self.rd = 0
		self.rs1 = 0
		self.rs2 = 0
		self.imm = 0

    def decodeI(self,machine_code):
        inst_list = []
        machine_code = machine_code >> 7
        inst_list.append((machine_code & 0x1f))    #rd
        machine_code = machine_code >> 5
        inst_list.append((machine_code & 0x3))     #funct3
        machine_code = machine_code >> 3
        inst_list.append((machine_code & 0x1f))    #rs1
        machine_code = machine_code >> 5
        inst_list.append((-(machine_code & 0x800) | (machine_code & 0x7ff)))    #imm(signed)
        #print(inst_list)
        return inst_list

    
    def decodeS(self,machine_code):
        inst_list = []
        machine_code = machine_code >> 7
        temp1 = machine_code & 0x1f     #building the register in temp1
        machine_code = machine_code >> 5
        inst_list.append((machine_code & 0x3))  #funct3
        machine_code = machine_code >> 3
        inst_list.append((machine_code & 0x1f)) #rs1
        machine_code = machine_code >> 5
        inst_list.append((machine_codep & 0x1f)) #rs2
        machine_code = machine_code >> 5
        machine_code = machine_code << 5
        temp1 = temp1+machine_code
        inst_list.append((-(temp1 & 0x800) | (temp1 & 0x7ff)))    #imm(signed)
        return inst_list

    
    def decodeU(self,machine_code):
        inst_list = []
        machine_code = machine_code>> 7
        inst_list.append((machine_code & 0x1f))     #rd
        machine_code = machine_code >> 5
        inst_list.append((-(machine_code & 0x80000) | (machine_code & 0x7ffff)))    #upper-imm(signed)
        return inst_list

    def decodeR(self,machine_code):
        inst_list = []
        machine_code = machine_code >> 7
        inst_list.append((machine_code& 0x1f))    #rd
        machine_code = machine_code >> 5
        inst_list.append((machine_code & 0x3))    #funct3
        machine_code = machine_code >> 3
        inst_list.append((machine_code & 0x1f))    #rs1
        machine_code = machine_code >> 5
        inst_list.append((machine_code & 0x1f))    #rs2
        machine_code= machine_code >> 5
        inst_list.append((machine_code & 0x7f))    #funct7
        return inst_list

    def decodeSB(self,machine_code):
        inst_list = []
        func3=machine_code & 0x000007000
        func3=func3>>12
        inst_list.append(func3) #funct3
        r1=machine_code & 0x000F8000
        r1=r1>>15
        inst_list.append(r1)  #rs1
        r2=machine_code & 0x01F00000
        r2=r2>>20
        inst_list.append(r2)   #rs2
        temp=machine_code>>7
        temp11=temp & 0x01   #imm[11]
        temp11=temp11<<11
        temp1=machine_code>>8
        temp1=temp1 & 0x0F  #imm[4:1]
        temp1=temp1<<1
        temp5=machine_code>>25
        temp5=temp5 & 0x03F  #imm[10:5]
        temp5=temp5<<5
        temp12=machine_code>>31
        temp12=temp12<<12   #imm[12]
        immf=temp12+temp11+temp5+temp1  #finding final imm
        im=(-(immf & 0x1000)| (immf& 0x0FFF))  #making it signed
        inst_list.append(im)
        return inst_list

    def decodeUJ(self,machine_code):
        inst_list = []
        rdd=machine_code & 0x00000F80
        rdd=rdd>>7
        inst_list.append(rdd)   #rd
        temp12=machine_code>>12
        temp12=temp12 & 0x0FF
        temp12=temp12<<12  #imm[19:12]
        temp11=machine_code>>20
        temp11=temp11 & 0x01
        temp11=temp11<<11  #imm[11]
        temp1=machine_code>>21
        temp1=temp1 & 0x03FF
        temp1=temp1<<1   #imm[10:1]
        temp20=machine_code>>31
        temp20=temp20<<20  #immp[20]
        immf=temp20+temp12+temp11+temp1  #final imm
        im=(-(immf & 0x100000)|(immf & 0x0FFFFF));  #making it signed
        inst_list.append(im)
        return inst_list

    def decode(self,hex_string): # hex_string==IR
        machine_code = hex_string
        self.opcode = (machine_code& 0x7f)
        #print(opcode, temp)
        if self.opcode in I:
            inst_list = self.decodeI(machine_code)
            self.rd = inst_list[0]
            self.funct3 = inst_list[1]
            self.rs1 = inst_list[2]
            self.imm = inst_list[3]
            #print(PC, "I type", opcode, funct3, rs1, rd, imm)
        elif self.opcode in S:
            inst_list = self.decodeS(machine_code)
            self.funct3 = inst_list[0]
            self.rs1 = inst_list[1]
            self.rs2 = inst_list[2]
            self.imm = inst_list[3]
            #print(PC, "S type", opcode, funct3, rs1, rs2, imm)
        elif self.opcode in U:
            inst_list = self.decodeU(machine_code)
            self.rd = inst_list[0]
            self.imm = inst_list[1]
            #print(PC, "U type", opcode, rd, imm)
        elif self.opcode in R:
            inst_list = self.decodeR(machine_code)
            self.rd = inst_list[0]
            self.funct3 = inst_list[1]
            self.rs1 = inst_list[2]
            self.rs2 = inst_list[3]
            self.funct7 = inst_list[4]
            #print(PC, "R type", opcode, funct3, funct7, rs1, rs2, rd)
        elif self.opcode in SB:
            inst_list = self.decodeSB(machine_code)
            self.funct3 = inst_list[0]
            self.rs1 = inst_list[1]
            self.rs2 = inst_list[2]
            self.imm = inst_list[3]
            #print(PC, "SB type", opcode, funct3, rs1, rs2, imm)
        elif self.opcode in UJ:
            inst_list = self.decodeUJ(machine_code)
            self.rd = inst_list[0]
            self.imm = inst_list[1]
            #print(PC, "UJ type", opcode, rd, imm)
        else:
            raise Exception("Not an instruction")

#circuit = ControlModule()
