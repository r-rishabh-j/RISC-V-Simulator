#!/usr/bin/python3
# generates control signals for the ALU and muxes 
import math

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
        self.BytesToRead = 0  # for the memory
        self.BytesToWrite = 0  # for the memory
        self.MuxINCSelect = 0  # to IAG, 0 for 4(sequential next), 1 for branch offset(imm)
        self.MuxPCSelect = 0  # to IAG
        self.MuxYSelect = 0  # present at output of ALU
        self.branch = 0  # signal to enforce checking output of ALU since branches are conditional
        self.jump = 0  # for jump signals(see doc)
        # 0- RZ
        # 1- MDR
        # 2- Return address from PC # PC has to be incremented in fetch stage itself
        self.MuxBSelect  # present at 2nd input of ALU
        # 0- rs2
        # 1- imm
        self.MuxMASelect  # Present at address input of memory
        self.MuxMDRSelect  # present at output of memory
        # self.decoder=DecodeModule()

    def controlStateUpdate(self): # will be called in each of 5 stages to release control signals specific to that stage


    def Interpret_UJ(self):
        self.MemRead = False #Mem is not Read in jal
        self.MemWrite = False #mem is not written to in jal
        self.ALUop = 0  #ALU is not used in jal
        self.RegWrite = 1 #PC value is written to register
        self.IRwrite = 0
        self.PCwrite = 1 # PC has to be updated in Jump
        self.BytesToRead = 0 #don't care
        self.BytesToWrite = 0 #don't care
        self.MuxINCSelect = 1 #Branch offset in used in IAG instead of 4
        self.MuxPCSelect = 1 #PC is selected instead of base address
        self.MuxYSelect = 2 #ra given to MuxY
        self.branch = 0
        self.jump = 1
        self.MuxBSelect = 0 # don't cares
        self.MuxMASelect = 0 # don't cares
        self.MuxMDRSelect = 0 # don't cares

    def Interpret_U(self):
        if self.opcode == 23:
        # print("auipc")
            self.MemRead = False #no memory read/write
            self.MemWrite = False
            self.ALUop = 1 #ALU is used to add to PC
            self.RegWrite = 1 #Register is updated
            self.IRwrite = 0
            self.PCwrite = 0
            self.BytesToRead = 0 # no memory access
            self.BytesToWrite = 0 # no memory access
            self.MuxINCSelect = 0 # 4 is chosen
            self.MuxPCSelect = 0 # PC is chosen, move sequentially next PC
            self.MuxYSelect = 0 # ALU output is chosen
            self.branch = 0
            self.jump = 0
            self.MuxBSelect = 1 # immediate selected
            self.MuxMASelect = 0 # don't care
            self.MuxMDRSelect = 0 # don't care
        elif self.opcode == 55:
        # print("lui")
            self.MemRead = False #no memory access
            self.MemWrite = False #no memory access
            self.ALUop = 1 # AlU is used
            self.RegWrite = 1 # Register is written to
            self.IRwrite = 0
            self.PCwrite = 0
            self.BytesToRead = 0 #don't care
            self.BytesToWrite = 0 #don't care
            self.MuxINCSelect = 0 #4 is added to PC
            self.MuxPCSelect = 1 # Pc is chosen
            self.MuxYSelect = 0 # ALU output is chosen
            self.branch = 0
            self.jump = 0
            self.MuxBSelect = 1 #imm is chosen
            self.MuxMASelect = 0 #don't care
            self.MuxMDRSelect = 0 #don't care

    def Interpret_S(self):
        if self.funct3 == 0:
        # print("sb")
            self.MemRead = False
            self.MemWrite = True #Mem is written to
            self.ALUop = 1 #ALU is used to get address
            self.RegWrite = 0 #Register is not written to
            self.IRwrite = 0
            self.PCwrite = 0
            self.BytesToRead = 0 #don't care
            self.BytesToWrite = 1
            self.MuxINCSelect = 0
            self.MuxPCSelect = 1
            self.MuxYSelect = 0
            self.branch = 0
            self.jump = 0
            self.MuxBSelect = 1 #imm is used
            self.MuxMASelect = 0 #rz is used
            self.MuxMDRSelect = 0 #not sure
        elif self.funct3 == 1:
        # print("sh")
            self.MemRead = False
            self.MemWrite = True  # Mem is written to
            self.ALUop = 1  # ALU is used to get address
            self.RegWrite = 0  # Register is not written to
            self.IRwrite = 0
            self.PCwrite = 0
            self.BytesToRead = 0  # don't care
            self.BytesToWrite = 2
            self.MuxINCSelect = 0
            self.MuxPCSelect = 1
            self.MuxYSelect = 0
            self.branch = 0
            self.jump = 0
            self.MuxBSelect = 1  # imm is used
            self.MuxMASelect = 0  # rz is used
            self.MuxMDRSelect = 0  # not sure
        elif self.funct3 == 2:
            self.MemRead = False
            self.MemWrite = True  # Mem is written to
            self.ALUop = 1  # ALU is used to get address
            self.RegWrite = 0  # Register is not written to
            self.IRwrite = 0
            self.PCwrite = 0
            self.BytesToRead = 0  # don't care
            self.BytesToWrite = 4
            self.MuxINCSelect = 0
            self.MuxPCSelect = 1
            self.MuxYSelect = 0
            self.branch = 0
            self.jump = 0
            self.MuxBSelect = 1  # imm is used
            self.MuxMASelect = 0  # rz is used
            self.MuxMDRSelect = 0  # not sure

    # print("sw")

    def Interpret_SB(self):
        if self.funct3 == 0:
        # print("beq")
        elif self.funct3 == 1:
        # print("bne")
        elif self.funct3 == 4:
        # print("blt")
        elif self.funct3 == 5:

    # print("bge")

    def Interpret_I(self):
        if self.opcode == 19:
            if self.funct3 == 0:
            # print("addi")
                self.MemRead = False
                self.MemWrite = False
                self.ALUop = 1
                self.RegWrite = 1
                self.IRwrite = 0
                self.PCwrite = 0
                self.BytesToRead = 0
                self.BytesToWrite = 0
                self.MuxINCSelect = 0
                self.MuxPCSelect = 1
                self.MuxYSelect = 0
                self.branch = 0
                self.jump = 0
                self.MuxBSelect = 1
                self.MuxMASelect = 0
                self.MuxMDRSelect = 0
            elif self.funct3 == 7:
            # print("andi")
                self.MemRead = False
                self.MemWrite = False
                self.ALUop = 1
                self.RegWrite = 1
                self.IRwrite = 0
                self.PCwrite = 0
                self.BytesToRead = 0
                self.BytesToWrite = 0
                self.MuxINCSelect = 0
                self.MuxPCSelect = 1
                self.MuxYSelect = 0
                self.branch = 0
                self.jump = 0
                self.MuxBSelect = 1
                self.MuxMASelect = 0
                self.MuxMDRSelect = 0
            elif self.funct3 == 6:
            # print("ori")
                self.MemRead = False
                self.MemWrite = False
                self.ALUop = 1
                self.RegWrite = 1
                self.IRwrite = 0
                self.PCwrite = 0
                self.BytesToRead = 0
                self.BytesToWrite = 0
                self.MuxINCSelect = 0
                self.MuxPCSelect = 1
                self.MuxYSelect = 0
                self.branch = 0
                self.jump = 0
                self.MuxBSelect = 1
                self.MuxMASelect = 0
                self.MuxMDRSelect = 0
        elif self.opcode == 3:
            if self.funct3 == 0:
            # print("lb")
                self.MemRead = False
                self.MemWrite = False
                self.ALUop = 1
                self.RegWrite = 1
                self.IRwrite = 0
                self.PCwrite = 0
                self.BytesToRead = 0
                self.BytesToWrite = 0
                self.MuxINCSelect = 0
                self.MuxPCSelect = 0
                self.MuxYSelect = 0
                self.branch = 0
                self.jump = 0
                self.MuxBSelect = 1
                self.MuxMASelect = 0
                self.MuxMDRSelect = 0
            elif self.funct3 == 1:
            # print("lh")
                self.MemRead = False
                self.MemWrite = False
                self.ALUop = 1
                self.RegWrite = 1
                self.IRwrite = 0
                self.PCwrite = 0
                self.BytesToRead = 0
                self.BytesToWrite = 0
                self.MuxINCSelect = 0
                self.MuxPCSelect = 0
                self.MuxYSelect = 0
                self.branch = 0
                self.jump = 0
                self.MuxBSelect = 1
                self.MuxMASelect = 0
                self.MuxMDRSelect = 0
            elif self.funct3 == 2:
            # print("lw")
                self.MemRead = False
                self.MemWrite = False
                self.ALUop = 1
                self.RegWrite = 1
                self.IRwrite = 0
                self.PCwrite = 0
                self.BytesToRead = 0
                self.BytesToWrite = 0
                self.MuxINCSelect = 0
                self.MuxPCSelect = 0
                self.MuxYSelect = 0
                self.branch = 0
                self.jump = 0
                self.MuxBSelect = 0
                self.MuxMASelect = 0
                self.MuxMDRSelect = 0
        elif self.opcode == 103:
        # print("jalr")
            self.MemRead = False
            self.MemWrite = False
            self.ALUop = 1
            self.RegWrite = 1
            self.IRwrite = 0
            self.PCwrite = 0
            self.BytesToRead = 0
            self.BytesToWrite = 0
            self.MuxINCSelect = 0
            self.MuxPCSelect = 0
            self.MuxYSelect = 0
            self.branch = 0
            self.jump = 0
            self.MuxBSelect = 0
            self.MuxMASelect = 0
            self.MuxMDRSelect = 0

    def Interpret_R(self):
        if self.funct3 == 0 and self.funct7 == 0:
            #print("add")
            self.MemRead = False
            self.MemWrite = False
            self.ALUop = 1
            self.RegWrite = 1
            self.IRwrite = 0
            self.PCwrite = 0
            self.BytesToRead = 0
            self.BytesToWrite = 0
            self.MuxINCSelect = 0
            self.MuxPCSelect = 0
            self.MuxYSelect = 0
            self.branch= 0
            self.jump = 0
            self.MuxBSelect = 0
            self.MuxMASelect = 0
            self.MuxMDRSelect = 0

        elif self.funct3 == 7 and self.funct7 == 0:
            # print("and")
            self.MemRead = False
            self.MemWrite = False
            self.ALUop = 1
            self.RegWrite = 1
            self.IRwrite = 0
            self.PCwrite = 0
            self.BytesToRead = 0
            self.BytesToWrite = 0
            self.MuxINCSelect = 0
            self.MuxPCSelect = 0
            self.MuxYSelect = 0
            self.branch = 0
            self.jump = 0
            self.MuxBSelect = 0
            self.MuxMASelect = 0
            self.MuxMDRSelect = 0

        elif self.funct3 == 6 and self.funct7 == 0:
            # print("or")
            self.MemRead = False
            self.MemWrite = False
            self.ALUop = 1
            self.RegWrite = 1
            self.IRwrite = 0
            self.PCwrite = 0
            self.BytesToRead = 0
            self.BytesToWrite = 0
            self.MuxINCSelect = 0
            self.MuxPCSelect = 0
            self.MuxYSelect = 0
            self.branch = 0
            self.jump = 0
            self.MuxBSelect = 0
            self.MuxMASelect = 0
            self.MuxMDRSelect = 0

        elif self.funct3 == 1 and self.funct7 == 0:
            # print("sll")
            self.MemRead = False
            self.MemWrite = False
            self.ALUop = 1
            self.RegWrite = 1
            self.IRwrite = 0
            self.PCwrite = 0
            self.BytesToRead = 0
            self.BytesToWrite = 0
            self.MuxINCSelect = 0
            self.MuxPCSelect = 0
            self.MuxYSelect = 0
            self.branch = 0
            self.jump = 0
            self.MuxBSelect = 0
            self.MuxMASelect = 0
            self.MuxMDRSelect = 0

        elif self.funct3 == 2 and self.funct7 == 0:
            # print("slt")
            self.MemRead = False
            self.MemWrite = False
            self.ALUop = 1
            self.RegWrite = 1
            self.IRwrite = 0
            self.PCwrite = 0
            self.BytesToRead = 0
            self.BytesToWrite = 0
            self.MuxINCSelect = 0
            self.MuxPCSelect = 0
            self.MuxYSelect = 0
            self.branch = 0
            self.jump = 0
            self.MuxBSelect = 0
            self.MuxMASelect = 0
            self.MuxMDRSelect = 0

        elif self.funct3 == 5 and self.funct7 == 32:
            # print("sra")
            self.MemRead = False
            self.MemWrite = False
            self.ALUop = 1
            self.RegWrite = 1
            self.IRwrite = 0
            self.PCwrite = 0
            self.BytesToRead = 0
            self.BytesToWrite = 0
            self.MuxINCSelect = 0
            self.MuxPCSelect = 0
            self.MuxYSelect = 0
            self.branch = 0
            self.jump = 0
            self.MuxBSelect = 0
            self.MuxMASelect = 0
            self.MuxMDRSelect = 0
        elif self.funct3 == 5 and self.funct7 == 0:
            # print("srl")
            self.MemRead = False
            self.MemWrite = False
            self.ALUop = 1
            self.RegWrite = 1
            self.IRwrite = 0
            self.PCwrite = 0
            self.BytesToRead = 0
            self.BytesToWrite = 0
            self.MuxINCSelect = 0
            self.MuxPCSelect = 0
            self.MuxYSelect = 0
            self.branch = 0
            self.jump = 0
            self.MuxBSelect = 0
            self.MuxMASelect = 0
            self.MuxMDRSelect = 0
        elif self.funct3 == 0 and self.funct7 == 32:
            # print("sub")
            self.MemRead = False
            self.MemWrite = False
            self.ALUop = 1
            self.RegWrite = 1
            self.IRwrite = 0
            self.PCwrite = 0
            self.BytesToRead = 0
            self.BytesToWrite = 0
            self.MuxINCSelect = 0
            self.MuxPCSelect = 0
            self.MuxYSelect = 0
            self.branch = 0
            self.jump = 0
            self.MuxBSelect = 0
            self.MuxMASelect = 0
            self.MuxMDRSelect = 0
        elif self.funct3 == 4 and self.funct7 == 0:
            # print("xor")
            self.MemRead = False
            self.MemWrite = False
            self.ALUop = 1
            self.RegWrite = 1
            self.IRwrite = 0
            self.PCwrite = 0
            self.BytesToRead = 0
            self.BytesToWrite = 0
            self.MuxINCSelect = 0
            self.MuxPCSelect = 0
            self.MuxYSelect = 0
            self.branch = 0
            self.jump = 0
            self.MuxBSelect = 0
            self.MuxMASelect = 0
            self.MuxMDRSelect = 0
        elif self.funct3 == 0 and self.funct7 == 1:
            # print("mul")
            self.MemRead = False
            self.MemWrite = False
            self.ALUop = 1
            self.RegWrite = 1
            self.IRwrite = 0
            self.PCwrite = 0
            self.BytesToRead = 0
            self.BytesToWrite = 0
            self.MuxINCSelect = 0
            self.MuxPCSelect = 0
            self.MuxYSelect = 0
            self.branch = 0
            self.jump = 0
            self.MuxBSelect = 0
            self.MuxMASelect = 0
            self.MuxMDRSelect = 0
        elif self.funct3 == 4 and self.funct7 == 1:
            # print("div")
            self.MemRead = False
            self.MemWrite = False
            self.ALUop = 1
            self.RegWrite = 1
            self.IRwrite = 0
            self.PCwrite = 0
            self.BytesToRead = 0
            self.BytesToWrite = 0
            self.MuxINCSelect = 0
            self.MuxPCSelect = 0
            self.MuxYSelect = 0
            self.branch = 0
            self.jump = 0
            self.MuxBSelect = 0
            self.MuxMASelect = 0
            self.MuxMDRSelect = 0
        elif self.funct3 == 6 and self.funct7 == 1:
            # print("rem")
            self.MemRead = False
            self.MemWrite = False
            self.ALUop = 1
            self.RegWrite = 1
            self.IRwrite = 0
            self.PCwrite = 0
            self.BytesToRead = 0
            self.BytesToWrite = 0
            self.MuxINCSelect = 0
            self.MuxPCSelect = 0
            self.MuxYSelect = 0
            self.branch = 0
            self.jump = 0
            self.MuxBSelect = 0
            self.MuxMASelect = 0
            self.MuxMDRSelect = 0

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
            self.Interpret_I()
        elif self.opcode in S:
            inst_list = self.decodeS(machine_code)
            self.funct7 = 0
            self.rd = 0
            self.funct3 = inst_list[0]
            self.rs1 = inst_list[1]
            self.rs2 = inst_list[2]
            self.imm = inst_list[3]
            # print(PC, "S type", opcode, funct3, rs1, rs2, imm)
            self.Interpret_S()
        elif self.opcode in U:
            inst_list = self.decodeU(machine_code)
            self.funct3 = 0
            self.funct7 = 0
            self.rs1 = 0
            self.rs2 = 0
            self.rd = inst_list[0]
            self.imm = inst_list[1]
            # print(PC, "U type", opcode, rd, imm)
            self.Interpret_U()
        elif self.opcode in R:
            inst_list = self.decodeR(machine_code)
            self.imm = 0
            self.rd = inst_list[0]
            self.funct3 = inst_list[1]
            self.rs1 = inst_list[2]
            self.rs2 = inst_list[3]
            self.funct7 = inst_list[4]
            # print(PC, "R type", opcode, funct3, funct7, rs1, rs2, rd)
            self.Interpret_R()
        elif self.opcode in SB:
            inst_list = self.decodeSB(machine_code)
            self.funct7 = 0
            self.rd = 0
            self.funct3 = inst_list[0]
            self.rs1 = inst_list[1]
            self.rs2 = inst_list[2]
            self.imm = inst_list[3]
            # print(PC, "SB type", opcode, funct3, rs1, rs2, imm)
            self.Interpret_SB()
        elif self.opcode in UJ:
            inst_list = self.decodeUJ(machine_code)
            self.funct3 = 0
            self.funct7 = 0
            self.rs1 = 0
            self.rs2 = 0
            self.rd = inst_list[0]
            self.imm = inst_list[1]
            # print(PC, "UJ type", opcode, rd, imm)
            self.Interpret_UJ()
        else:
            raise Exception("Not an instruction")

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
        if opcode == 51:
            if funct3 == 0:
                if funct7 == 0:
                    return 0
                elif funct7 == 32:
                    return 7
                elif funct7 == 1:
                    return 9
            elif funct3 == 7:
                if funct7 == 0:
                    return 1
            elif funct3 == 6:
                if funct7 == 0:
                    return 2
                elif funct7 == 1:
                    return 11
            elif funct3 == 1:
                return 3
            elif funct3 == 5:
                if funct7 == 0:
                    return 4
                elif funct7 == 32:
                    return 5
            elif funct3 == 2:
                if funct7 == 0:
                    return 6
            elif funct3 == 4:
                if funct7 == 0:
                    return 8
                elif funct7 == 1:
                    return 10
            else:
                raise Exception("Not a valid Instruction")
        elif opcode == 19:
            if funct3 == 0 and funct7 == 0:
                return 0
            elif funct3 == 7 and funct7 == 0:
                return 1
            elif funct3 == 6 and funct7 == 0:
                return 2
            else:
                raise Exception("Not a valid Instruction")
        elif opcode == 3:
            if funct3 in [0, 1, 2] and funct7 == 0:
                return 0
            else:
                raise Exception("Not a valid Instruction")
        elif opcode == 103:
            if funct3 == 0 and funct7 == 0:
                return 0
            else:
                raise Exception("Not a valid Instruction")
        elif opcode == 35:
            if funct3 in [0, 1, 2] and funct7 == 0:
                return 0
            else:
                raise Exception("Not a valid Instruction")
        elif opcode == 23:
            if funct3 == 0 and funct7 == 0:
                return 12
            else:
                raise Exception("Not a valid Instruction")
        elif opcode == 55:
            if funct3 == 0 and funct7 == 0:
                return 12
            else:
                raise Exception("Not a valid Instruction")
        elif opcode == 111:
            if funct3 == 0 and funct7 == 0:
                return 0
            else:
                raise Exception("Not a valid Instruction")
        elif opcode == 99:
            if funct3 == 0 and funct7 == 0:
                return 13
            elif funct3 == 1 and funct7 == 0:
                return 14
            elif funct3 == 5 and funct7 == 0:
                return 15
            elif funct3 == 4 and funct7 == 0:
                return 16
            else:
                raise Exception("Not a valid Instruction")
        else:
            raise Exception("Not a valid Instruction")

    # def getOpcode(self):
    #     return self.opcode
    # def getFunct3(self):
    #     return self.funct3
    # def getFunct7(self):
    #     return self.funct7
    # def getRd(self):
    #     return self.rd
    # def getRs1(self):
    #     return self.rs1
    # def getRs2(self):
    #     return self.rs2
    # def getImm(self):
    #     return self.imm

    # def setOpcode(self, opcode):
    #     self.opcode = opcode
    # def setFunct3(self, funct3):
    #     self.funct3 = funct3
    # def setFunct7(self, funct7):
    #     self.funct7 = funct7
    # def setRd(self, rd):
    #     self.rd = rd
    # def setRs1(self, rs1):
    #     self.rs1 = rs1
    # def setRs2(self, rs2):
    #     self.rs2 = rs2
    # def setImm(self, imm):
    #     self.imm = imm

# class DecodeModule:
#     def __init__(self):
#         self.opcode = 0
#         self.funct3 = 0
#         self.funct7 = 0
#         self.rd = 0
#         self.rs1 = 0
#         self.rs2 = 0
#         self.imm = 0

#     def decodeI(self,machine_code):
#         inst_list = []
#         machine_code = machine_code >> 7
#         inst_list.append((machine_code & 0x1f))    #rd
#         machine_code = machine_code >> 5
#         inst_list.append((machine_code & 0x3))     #funct3
#         machine_code = machine_code >> 3
#         inst_list.append((machine_code & 0x1f))    #rs1
#         machine_code = machine_code >> 5
#         inst_list.append((-(machine_code & 0x800) | (machine_code & 0x7ff)))    #imm(signed)
#         #print(inst_list)
#         return inst_list


#     def decodeS(self,machine_code):
#         inst_list = []
#         machine_code = machine_code >> 7
#         temp1 = machine_code & 0x1f     #building the register in temp1
#         machine_code = machine_code >> 5
#         inst_list.append((machine_code & 0x3))  #funct3
#         machine_code = machine_code >> 3
#         inst_list.append((machine_code & 0x1f)) #rs1
#         machine_code = machine_code >> 5
#         inst_list.append((machine_codep & 0x1f)) #rs2
#         machine_code = machine_code >> 5
#         machine_code = machine_code << 5
#         temp1 = temp1+machine_code
#         inst_list.append((-(temp1 & 0x800) | (temp1 & 0x7ff)))    #imm(signed)
#         return inst_list


#     def decodeU(self,machine_code):
#         inst_list = []
#         machine_code = machine_code>> 7
#         inst_list.append((machine_code & 0x1f))     #rd
#         machine_code = machine_code >> 5
#         inst_list.append((-(machine_code & 0x80000) | (machine_code & 0x7ffff)))    #upper-imm(signed)
#         return inst_list

#     def decodeR(self,machine_code):
#         inst_list = []
#         machine_code = machine_code >> 7
#         inst_list.append((machine_code& 0x1f))    #rd
#         machine_code = machine_code >> 5
#         inst_list.append((machine_code & 0x3))    #funct3
#         machine_code = machine_code >> 3
#         inst_list.append((machine_code & 0x1f))    #rs1
#         machine_code = machine_code >> 5
#         inst_list.append((machine_code & 0x1f))    #rs2
#         machine_code= machine_code >> 5
#         inst_list.append((machine_code & 0x7f))    #funct7
#         return inst_list

#     def decodeSB(self,machine_code):
#         inst_list = []
#         func3=machine_code & 0x000007000
#         func3=func3>>12
#         inst_list.append(func3) #funct3
#         r1=machine_code & 0x000F8000
#         r1=r1>>15
#         inst_list.append(r1)  #rs1
#         r2=machine_code & 0x01F00000
#         r2=r2>>20
#         inst_list.append(r2)   #rs2
#         temp=machine_code>>7
#         temp11=temp & 0x01   #imm[11]
#         temp11=temp11<<11
#         temp1=machine_code>>8
#         temp1=temp1 & 0x0F  #imm[4:1]
#         temp1=temp1<<1
#         temp5=machine_code>>25
#         temp5=temp5 & 0x03F  #imm[10:5]
#         temp5=temp5<<5
#         temp12=machine_code>>31
#         temp12=temp12<<12   #imm[12]
#         immf=temp12+temp11+temp5+temp1  #finding final imm
#         im=(-(immf & 0x1000)| (immf& 0x0FFF))  #making it signed
#         inst_list.append(im)
#         return inst_list

#     def decodeUJ(self,machine_code):
#         inst_list = []
#         rdd=machine_code & 0x00000F80
#         rdd=rdd>>7
#         inst_list.append(rdd)   #rd
#         temp12=machine_code>>12
#         temp12=temp12 & 0x0FF
#         temp12=temp12<<12  #imm[19:12]
#         temp11=machine_code>>20
#         temp11=temp11 & 0x01
#         temp11=temp11<<11  #imm[11]
#         temp1=machine_code>>21
#         temp1=temp1 & 0x03FF
#         temp1=temp1<<1   #imm[10:1]
#         temp20=machine_code>>31
#         temp20=temp20<<20  #immp[20]
#         immf=temp20+temp12+temp11+temp1  #final imm
#         im=(-(immf & 0x100000)|(immf & 0x0FFFFF));  #making it signed
#         inst_list.append(im)
#         return inst_list

#     def decode(self,hex_string): # hex_string==IR
#         machine_code = hex_string
#         self.opcode = (machine_code& 0x7f)
#         #print(opcode, temp)
#         if self.opcode in I:
#             inst_list = self.decodeI(machine_code)
#             self.funct7 = 0
#             self.rs1 = 0
#             self.rd = inst_list[0]
#             self.funct3 = inst_list[1]
#             self.rs1 = inst_list[2]
#             self.imm = inst_list[3]
#             #print(PC, "I type", opcode, funct3, rs1, rd, imm)
#         elif self.opcode in S:
#             inst_list = self.decodeS(machine_code)
#             self.funct7 = 0
#             self.rd = 0
#             self.funct3 = inst_list[0]
#             self.rs1 = inst_list[1]
#             self.rs2 = inst_list[2]
#             self.imm = inst_list[3]
#             #print(PC, "S type", opcode, funct3, rs1, rs2, imm)
#         elif self.opcode in U:
#             inst_list = self.decodeU(machine_code)
#             self.funct3 = 0
#             self.funct7 = 0
#             self.rs1 = 0
#             self.rs2 = 0
#             self.rd = inst_list[0]
#             self.imm = inst_list[1]
#             #print(PC, "U type", opcode, rd, imm)
#         elif self.opcode in R:
#             inst_list = self.decodeR(machine_code)
#             self.imm = 0
#             self.rd = inst_list[0]
#             self.funct3 = inst_list[1]
#             self.rs1 = inst_list[2]
#             self.rs2 = inst_list[3]
#             self.funct7 = inst_list[4]
#             #print(PC, "R type", opcode, funct3, funct7, rs1, rs2, rd)
#         elif self.opcode in SB:
#             inst_list = self.decodeSB(machine_code)
#             self.funct7 = 0
#             self.rd = 0
#             self.funct3 = inst_list[0]
#             self.rs1 = inst_list[1]
#             self.rs2 = inst_list[2]
#             self.imm = inst_list[3]
#             #print(PC, "SB type", opcode, funct3, rs1, rs2, imm)
#         elif self.opcode in UJ:
#             inst_list = self.decodeUJ(machine_code)
#             self.funct3 = 0
#             self.funct7 = 0
#             self.rs1 = 0
#             self.rs2 = 0
#             self.rd = inst_list[0]
#             self.imm = inst_list[1]
#             #print(PC, "UJ type", opcode, rd, imm)
#         else:
#             raise Exception("Not an instruction")

# circuit = ControlModule()
