#!/usr/bin/python3
# generates control signals for the ALU and muxes 
import math
import sys

# addi 19 0
# andi 19 7
# ori 19 6
# lb 3 0
# lh 3 1
# lw 3 2
# jalr 103 0
I = [19, 3, 103]  # opcodes for I

# sb 35 0
# sh 35 1
# sw 35 2
S = [35]  # opcode for S

# auipc 23
# lui 55
U = [23, 55]  # opcodes for U

# add 51 0 0
# and 51 7 0
# or 51 6 0
# sll 51 1 0
# slt 51 2 0
# sra 51 5 32
# srl 51 5 0
# sub 51 0 32
# xor 51 4 0
# mul 51 0 1
# div 51 4 1
# rem 51 6 1
R = [51]  # opcode for R
SB = [99]  # opcode for SB
UJ = [111]  # opcode for UJ
MAX_SIGNED_NUM = 0x7fffffff
MIN_SIGNED_NUM = -0x80000000
MAX_UNSIGNED_NUM = 0xffffffff
MIN_UNSIGNED_NUM = 0x00000000

class ControlModule:
    def __init__(self):
        self.opcode = 0
        self.funct3 = 0
        self.funct7 = 0
        self.rd = 0
        self.rs1 = 0
        self.rs2 = 0
        self.imm = 0  # for imm12, imm5, imm20, imm13
        self.MemRead = False
        self.MemWrite = False
        self.ALUop = 0  # to use ALU or not
        self.ALUcontrol=0
        self.RegWrite = 0  # 1-to update the register(write back stage)
        self.IRwrite = 0
        self.PCwrite = 0
        # self.BytesToRead = 0  # for the memory
        # self.BytesToWrite = 0  # for the memory
        self.BytesToAccess=0 # memory access
        self.MuxINCSelect = 0  # to IAG, 0 for 4(sequential next), 1 for branch offset(imm)
        self.MuxPCSelect = 0  # to IAG, 0 for ra and 1 for normal PC
        self.MuxYSelect = 0  # present at output of ALU
        self.MuxAselect=0
        self.branch = 0  # signal to enforce checking output of ALU since branches are conditional
        self.jump = 0  # for jump signals(see doc)
        self.MuxBSelect=0  # present at 2nd input of ALU
        self.MuxASelect = 0
        # 0- RZ
        # 1- MDR
        # 2- Return address from PC # PC has to be incremented in fetch stage itself
        # 0- rs2
        # 1- imm
        # self.MuxMASelect  # Present at address input of memory
        # self.MuxMDRSelect  # present at output of memory
        # self.decoder=DecodeModule()

    def controlStateUpdate(self): # for stage dependant control signals

    def ControlSignalGenerator(self):
        if self.opcode == 51:  #R-type
            self.ALUOp = 1  #ALU usage required
            self.RegWrite = 1  #update register
            self.MemRead = False
            self.MemWrite = False
            self.branch = 0  #required to update control for branch inst
            self.jump=0
            self.MuxASelect = 0      #rs1
            self.MuxBSelect = 0  #no immediate
            self.MuxYSelect = 0  #choose output of ALU in RZ
            self.MuxPCSelect = 1     #not ra
            self.BytesToAccess = 0
            #self.BytestoWrite = 0
            self.MuxINCSelect = 0    #sequentially next PC
            #self.#MuxMASelect = 1     #PC send to MAR in step1
        elif self.opcode == 19:    #I-type (ori, andi, addi)
            self.ALUOp = 1
            self.RegWrite = 1    #update register
            self.MemRead = False
            self.MemWrite = False
            self.branch = 0          #required to update control for branch inst
            self.jump = 0          #required to update control for jump inst
            self.MuxASelect = 0      #rs1
            self.MuxBSelect = 1   #imm value used in MuxB
            self.MuxYSelect = 0    #choose output of ALU in RZ
            self.MuxPCSelect = 1     #not ra
            self.BytesToAccess=0
            # self.BytestoRead = 0
            # self.BytestoWrite = 0
            self.MuxINCSelect = 0    #sequentially next PC
            #self.#MuxMASelect = 1     #PC send to MAR in step1
        elif opcode == 3:   #I-type(load-instructions)
            self.ALUOp = 1       #ALU used to calculate effective address
            self.RegWrite = 1    #update register
            self.MemRead = True
            self.MemWrite = False
            if self.funct3 == 0:   #lb
                self.BytesToAccess = 1
            elif self.funct3 == 1:   #lh
                self.BytesToAccess = 2
            elif self.funct3 == 2:   #lw
                self.BytesToAccess = 4
            else:
                raise Exception("Invalid funct3")
            #self.BytestoWrite = 0
            self.MuxINCSelect = 0  #sequentially next PC
            self.MuxASelect = 0  # rs1
            self.MuxBSelect = 1  # imm value used in MuxB
            self.MuxYSelect = 1  # MDR value selected
            self.branch = 0 #required to update control for branch inst
            self.jump = 0 #required to update control for jump inst
            self.MuxPCSelect = 1 # not ra
            #MuxMASelect = 1     #PC send to MAR in step1
        elif self.opcode == 103:     #I-type(jalr)
            self.ALUOp = 0   #ALU not used, done in IAG
            self.MuxBSelect = 0  #don't-care
            self.MuxYSelect = 2  #ra given to MuxY
            # self.BytestoRead = 0
            # self.BytestoWrite = 0
            self.BytesToAccess=0
            self.RegWrite = 1    #update register
            self.MuxINCSelect = 1 # receive imm
            self.MuxASelect = 0      #rs1
            self.branch = 0          #required to update control for branch inst
            self.jump=1 # jump instruction
            self.MuxPCSelect = 0     #ra input to MuxPC
            self.MemRead = False
            self.MemWrite = False
            #MuxMASelect = 1     #PC send to MAR in step1
        elif opcode == 35:      #S-type
            self.ALUOp = 1   #ALU used to calculate effective address
            self.MuxBSelect = 1  #imm value used in MuxB
            self.MuxYSelect = 0  #don't-care
            #self.BytestoRead = 0
            if self.funct3 == 0: #sb
                self.BytesToAccess = 1
            elif self.funct3 == 1: #sh
                self.BytesToAccess = 2
            elif self.funct3 == 2: #sw
                self.BytesToAccess = 4
            else:
                raise Exception("Invalid funct3")
            self.RegWrite = 0    #Register update not required
            self.MuxINCSelect = 0    #sequentially next PC
            self.MuxASelect = 0      #rs1
            self.branch = 0          #required to update control for branch inst
            self.jump=0
            self.MuxPCSelect = 1     #not ra
            self.MemRead = False
            self.MemWrite = True
            #self.MuxMASelect = 1     #PC send to MAR in step1
        elif self.opcode == 23 :  #U-type(auipc)
            self.ALUOp = 1
            self.MuxBSelect = 1
            self.MuxYSelect = 0  #choose output of ALU in RZ
            # self.BytestoRead = 0
            # self.BytestoWrite = 0
            self.BytesToAccess=0
            self.RegWrite = 1
            self.MuxINCSelect = 0    #sequentially next PC
            self.MuxASelect = 1      #PC as input1 of ALU
            self.MuxPCSelect = 1     #not ra
            self.branch = 0          #required to update control for branch inst
            self.jump=0
            self.MemWrite = False
            self.MemRead = False
            #MuxMASelect = 1     #PC send to MAR in step1
        elif opcode == 55:  #U-type(lui)
            self.ALUOp = 1
            self.MuxBSelect = 1
            self.MuxYSelect = 0  #choose output of ALU in RZ
            # self.BytestoRead = 0
            # self.BytestoWrite = 0
            self.BytesToAccess=0
            self.RegWrite = 1
            self.MuxINCSelect = 0    #sequentially next PC(4)
            self.MuxASelect = 0      #rs1
            self.branch = 0          #required to update control for branch inst
            self.jump=0
            self.MuxPCSelect = 1     #not ra
            self.MemRead = False
            self.MemWrite = False
            #self.#MuxMASelect = 1     #PC send to MAR in step1
        elif self.opcode == 111: #UJ-type(jal)
            self.ALUOp = 0   #ALU not required, done in IAG
            self.MuxBSelect = 0  #don't-care
            self.MuxYSelect = 2  #ra given to MuxY
            # self.BytestoRead = 0
            # self.BytestoWrite = 0
            self.BytesToAccess=0
            self.RegWrite = 1    #update register
            self.MuxINCSelect = 1
            self.MuxASelect = 0      #rs1
            self.branch = 0          #required to update control for branch inst
            self.jump=1
            self.MuxPCSelect = 1     #not ra
            self.MemRead = False
            self.MemWrite = False
            #MuxMASelect = 1     #PC send to MAR in step1
        elif self.opcode == 99:  #SB type
            self.ALUOp = 1 # ALU computes boolean for branch
            self.MuxBSelect = 0  #rs2 is required, imm is used in IAG
            self.MuxYSelect = 0  #RZ, but don't-care
            self.RegWrite = 0    #do not update register
            # self.BytestoRead = 0
            # self.BytestoWrite = 0
            self.BytesToAccess=0
            self.MuxINCSelect = 0   #to be updated after ALU
            self.MuxASelect = 0      #rs1
            self.branch = 1          #required to update control for branch inst
            self.jump=0
            self.MuxPCSelect = 1     #not ra
            self.MemRead = False
            self.MemWrite = False
            #MuxMASelect = 1     #PC send to MAR in step1
        
    def decode(self, IR):
        machine_code = IR
        self.opcode = (machine_code & 0x7f)
        # print(opcode, temp)
        if self.opcode in I:
            inst_list = self.decodeI(machine_code)
            self.funct7 = 0
            self.rs1 = 0
            self.rd = inst_list[0]
            self.funct3 = inst_list[1]
            self.rs1 = inst_list[2]
            self.imm = inst_list[3]
            # print(PC, "I type", opcode, funct3, rs1, rd, imm)
            #self.Interpret_I()
        elif self.opcode in S:
            inst_list = self.decodeS(machine_code)
            self.funct7 = 0
            self.rd = 0
            self.funct3 = inst_list[0]
            self.rs1 = inst_list[1]
            self.rs2 = inst_list[2]
            self.imm = inst_list[3]
            # print(PC, "S type", opcode, funct3, rs1, rs2, imm)
            #self.Interpret_S()
        elif self.opcode in U:
            inst_list = self.decodeU(machine_code)
            self.funct3 = 0
            self.funct7 = 0
            self.rs1 = 0
            self.rs2 = 0
            self.rd = inst_list[0]
            self.imm = inst_list[1]
            # print(PC, "U type", opcode, rd, imm)
            #self.Interpret_U()
        elif self.opcode in R:
            inst_list = self.decodeR(machine_code)
            self.imm = 0
            self.rd = inst_list[0]
            self.funct3 = inst_list[1]
            self.rs1 = inst_list[2]
            self.rs2 = inst_list[3]
            self.funct7 = inst_list[4]
            # print(PC, "R type", opcode, funct3, funct7, rs1, rs2, rd)
            #self.Interpret_R()
        elif self.opcode in SB:
            inst_list = self.decodeSB(machine_code)
            self.funct7 = 0
            self.rd = 0
            self.funct3 = inst_list[0]
            self.rs1 = inst_list[1]
            self.rs2 = inst_list[2]
            self.imm = inst_list[3]
            # print(PC, "SB type", opcode, funct3, rs1, rs2, imm)
            #self.Interpret_SB()
        elif self.opcode in UJ:
            inst_list = self.decodeUJ(machine_code)
            self.funct3 = 0
            self.funct7 = 0
            self.rs1 = 0
            self.rs2 = 0
            self.rd = inst_list[0]
            self.imm = inst_list[1]
            # print(PC, "UJ type", opcode, rd, imm)
            #self.Interpret_UJ()
		elif self.opcode == 17:
			sys.exit("All instructions executed, end of program")

        else:
            raise Exception("Not an instruction")
        
        # generate control signals for ALU and other modules
        self.ControlSignalGenerator()
        self.ALUcontrol = self.ALUcontrolgenerator(self.opcode, self.funct3, self.funct7)

    def decodeI(self, machine_code):
        inst_list = []
        machine_code = machine_code >> 7
        inst_list.append((machine_code & 0x1f))  # rd
        machine_code = machine_code >> 5
        inst_list.append((machine_code & 0x3))  # funct3
        machine_code = machine_code >> 3
        inst_list.append((machine_code & 0x1f))  # rs1
        machine_code = machine_code >> 5
        inst_list.append((-(machine_code & 0x800) | (machine_code & 0x7ff)))  # imm(signed)
        # print(inst_list)
        return inst_list

    def decodeS(self, machine_code):
        inst_list = []
        machine_code = machine_code >> 7
        temp1 = machine_code & 0x1f  # building the register in temp1
        machine_code = machine_code >> 5
        inst_list.append((machine_code & 0x3))  # funct3
        machine_code = machine_code >> 3
        inst_list.append((machine_code & 0x1f))  # rs1
        machine_code = machine_code >> 5
        inst_list.append((machine_codep & 0x1f))  # rs2
        machine_code = machine_code >> 5
        machine_code = machine_code << 5
        temp1 = temp1 + machine_code
        inst_list.append((-(temp1 & 0x800) | (temp1 & 0x7ff)))  # imm(signed)
        return inst_list

    def decodeU(self, machine_code):
        inst_list = []
        machine_code = machine_code >> 7
        inst_list.append((machine_code & 0x1f))  # rd
        machine_code = machine_code >> 5
        inst_list.append((-(machine_code & 0x80000) | (machine_code & 0x7ffff)))  # upper-imm(signed)
        return inst_list

    def decodeR(self, machine_code):
        inst_list = []
        machine_code = machine_code >> 7
        inst_list.append((machine_code & 0x1f))  # rd
        machine_code = machine_code >> 5
        inst_list.append((machine_code & 0x3))  # funct3
        machine_code = machine_code >> 3
        inst_list.append((machine_code & 0x1f))  # rs1
        machine_code = machine_code >> 5
        inst_list.append((machine_code & 0x1f))  # rs2
        machine_code = machine_code >> 5
        inst_list.append((machine_code & 0x7f))  # funct7
        return inst_list

    def decodeSB(self, machine_code):
        inst_list = []
        func3 = machine_code & 0x000007000
        func3 = func3 >> 12
        inst_list.append(func3)  # funct3
        r1 = machine_code & 0x000F8000
        r1 = r1 >> 15
        inst_list.append(r1)  # rs1
        r2 = machine_code & 0x01F00000
        r2 = r2 >> 20
        inst_list.append(r2)  # rs2
        temp = machine_code >> 7
        temp11 = temp & 0x01  # imm[11]
        temp11 = temp11 << 11
        temp1 = machine_code >> 8
        temp1 = temp1 & 0x0F  # imm[4:1]
        temp1 = temp1 << 1
        temp5 = machine_code >> 25
        temp5 = temp5 & 0x03F  # imm[10:5]
        temp5 = temp5 << 5
        temp12 = machine_code >> 31
        temp12 = temp12 << 12  # imm[12]
        immf = temp12 + temp11 + temp5 + temp1  # finding final imm
        im = (-(immf & 0x1000) | (immf & 0x0FFF))  # making it signed
        inst_list.append(im)
        return inst_list

    def decodeUJ(self, machine_code):
        inst_list = []
        rdd = machine_code & 0x00000F80
        rdd = rdd >> 7
        inst_list.append(rdd)  # rd
        temp12 = machine_code >> 12
        temp12 = temp12 & 0x0FF
        temp12 = temp12 << 12  # imm[19:12]
        temp11 = machine_code >> 20
        temp11 = temp11 & 0x01
        temp11 = temp11 << 11  # imm[11]
        temp1 = machine_code >> 21
        temp1 = temp1 & 0x03FF
        temp1 = temp1 << 1  # imm[10:1]
        temp20 = machine_code >> 31
        temp20 = temp20 << 20  # immp[20]
        immf = temp20 + temp12 + temp11 + temp1  # final imm
        im = (-(immf & 0x100000) | (immf & 0x0FFFFF));  # making it signed
        inst_list.append(im)
        return inst_list

    def ALUcontrolgenerator(self, opcode, funct3, funct7):
        if self.opcode == 51:
            if self.funct3 == 0:
                if self.funct7 == 0:
                    return 0
                elif self.funct7 == 32:
                    return 7
                elif self.funct7 == 1:
                    return 9
            elif self.funct3 == 7:
                if self.funct7 == 0:
                    return 1
            elif self.funct3 == 6:
                if self.funct7 == 0:
                    return 2
                elif self.funct7 == 1:
                    return 11
            elif self.funct3 == 1:
                return 3
            elif self.funct3 == 5:
                if self.funct7 == 0:
                    return 4
                elif self.funct7 == 32:
                    return 5
            elif self.funct3 == 2:
                if self.funct7 == 0:
                    return 6
            elif self.funct3 == 4:
                if self.funct7 == 0:
                    return 8
                elif self.funct7 == 1:
                    return 10
            else:
                raise Exception("Not a valid Instruction")
        elif self.opcode == 19:
            if self.funct3 == 0 and self.funct7 == 0:
                return 0
            elif self.funct3 == 7 and self.funct7 == 0:
                return 1
            elif self.funct3 == 6 and self.funct7 == 0:
                return 2
            else:
                raise Exception("Not a valid Instruction")
        elif self.opcode == 3:
            if self.funct3 in [0, 1, 2] and self.funct7 == 0:
                return 0
            else:
                raise Exception("Not a valid Instruction")
        elif self.opcode == 103:
            if self.funct3 == 0 and self.funct7 == 0:
                return 0
            else:
                raise Exception("Not a valid Instruction")
        elif self.opcode == 35:
            if self.funct3 in [0, 1, 2] and self.funct7 == 0:
                return 0
            else:
                raise Exception("Not a valid Instruction")
        elif self.opcode == 23:
            if self.funct3 == 0 and self.funct7 == 0:
                return 12
            else:
                raise Exception("Not a valid Instruction")
        elif self.opcode == 55:
            if self.funct3 == 0 and self.funct7 == 0:
                return 12
            else:
                raise Exception("Not a valid Instruction")
        elif self.opcode == 111:
            if self.funct3 == 0 and self.funct7 == 0:
                return 0
            else:
                raise Exception("Not a valid Instruction")
        elif self.opcode == 99:
            if self.funct3 == 0 and self.funct7 == 0:
                return 13
            elif self.funct3 == 1 and self.funct7 == 0:
                return 14
            elif self.funct3 == 5 and self.funct7 == 0:
                return 15
            elif self.funct3 == 4 and self.funct7 == 0:
                return 16
            else:
                raise Exception("Not a valid Instruction")
        else:
            raise Exception("Not a valid Instruction")


    def branching_controlUpdate(self,outputBool):   # this function will help decide whether to jump or not in branching instructions based on ALU output
        if branch&jump==1:
            raise Exception("Invalid control signal")
        if self.branch==0:
            if self.jump==0:
                self.MuxINCSelect=0
            else:
                self.MuxINCSelect=1
        elif self.branch==1:
            if outputBool==1:
                self.MuxINCSelect=1
            else:
                self.MuxINCSelect=0
