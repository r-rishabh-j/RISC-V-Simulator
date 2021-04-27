# control signals generator
def ControlSignalGenerator(opcode, funct3):
    if opcode == 51:  # R-type
        ALUOp = 1  # ALU usage required
        MuxBSelect = 0  # no immediate
        MuxYSelect = 0  # choose output of ALU in RZ
        BytestoRead = 0
        BytestoWrite = 0
        RegWrite = 1  # update register
        MuxINCSelect = 0  # sequentially next PC
        MuxASelect = 0  # rs1
        branch = 0  # required to update control for branch inst
        MuxPCSelect = 1  # not ra
        # MuxMASelect = 1     #PC send to MAR in step1
        MemRead = False
        MemWrite = False
    elif opcode == 19:  # I-type (ori, andi, addi)
        ALUOp = 1
        MuxBSelect = 1  # imm value used in MuxB
        MuxYSelect = 0  # choose output of ALU in RZ
        BytestoRead = 0
        BytestoWrite = 0
        RegWrite = 1  # update register
        MuxINCSelect = 0  # sequentially next PC
        MuxASelect = 0  # rs1
        branch = 0  # required to update control for branch inst
        MuxPCSelect = 1  # not ra
        # MuxMASelect = 1     #PC send to MAR in step1
        MemRead = False
        MemWrite = False
    elif opcode == 3:  # I-type(load-instructions)
        ALUOp = 1  # ALU used to calculate effective address
        MuxBSelect = 1  # imm value used in MuxB
        MuxYSelect = 1  # MDR value selected
        if funct3 == 0:  # lb
            BytestoRead = 1
        if funct3 == 1:  # lh
            BytestoRead = 2
        if funct3 == 2:  # lw
            BytestoRead = 4
        BytestoWrite = 0
        RegWrite = 1  # update register
        MuxINCSelect = 0  # sequentially next PC
        MuxASelect = 0  # rs1
        branch = 0  # required to update control for branch inst
        MuxPCSelect = 1  # not ra
        # MuxMASelect = 1     #PC send to MAR in step1
        MemRead = True
        MemWrite = False
    elif opcode == 103:  # I-type(jalr)
        ALUOp = 0  # ALU not used, done in IAG
        MuxBSelect = 0  # don't-care
        MuxYSelect = 2  # ra given to MuxY
        BytestoRead = 0
        BytestoWrite = 0
        RegWrite = 1  # update register
        MuxINCSelect = 1
        MuxASelect = 0  # rs1
        branch = 0  # required to update control for branch inst
        MuxPCSelect = 0  # ra input to MuxPC
        # MuxMASelect = 1     #PC send to MAR in step1
        MemRead = False
        MemWrite = False
    elif opcode == 35:  # S-type
        ALUOp = 1  # ALU used to calculate effective address
        MuxBSelect = 1  # imm value used in MuxB
        MuxYSelect = 0  # don't-care
        BytestoRead = 0
        if funct3 == 0:  # sb
            BytestoWrite = 1
        if funct3 == 1:  # sh
            BytestoWrite = 2
        if funct3 == 2:  # sw
            BytestoWrite = 4
        RegWrite = 0  # Register update not required
        MuxINCSelect = 0  # sequentially next PC
        MuxASelect = 0  # rs1
        branch = 0  # required to update control for branch inst
        MuxPCSelect = 1  # not ra
        # MuxMASelect = 1     #PC send to MAR in step1
        MemRead = False
        MemWrite = True
    elif opcode == 23:  # U-type(auipc)
        ALUOp = 1
        MuxBSelect = 1
        MuxYSelect = 0  # choose output of ALU in RZ
        BytestoRead = 0
        BytestoWrite = 0
        RegWrite = 1
        MuxINCSelect = 0  # sequentially next PC
        MuxASelect = 1  # PC as input1 of ALU
        branch = 0  # required to update control for branch inst
        MuxPCSelect = 1  # not ra
        # MuxMASelect = 1     #PC send to MAR in step1
        MemRead = False
        MemWrite = False
    elif opcode == 55:  # U-type(lui)
        ALUOp = 1
        MuxBSelect = 1
        MuxYSelect = 0  # choose output of ALU in RZ
        BytestoRead = 0
        BytestoWrite = 0
        RegWrite = 1
        MuxINCSelect = 0  # sequentially next PC(4)
        MuxASelect = 0  # rs1
        branch = 0  # required to update control for branch inst
        MuxPCSelect = 1  # not ra
        # MuxMASelect = 1     #PC send to MAR in step1
        MemRead = False
        MemWrite = False
    elif opcode == 111:  # UJ-type(jal)
        ALUOp = 0  # ALU not required, done in IAG
        MuxBSelect = 0  # don't-care
        MuxYSelect = 2  # ra given to MuxY
        BytestoRead = 0
        BytestoWrite = 0
        RegWrite = 1  # update register
        MuxINCSelect = 1
        MuxASelect = 0  # rs1
        branch = 0  # required to update control for branch inst
        MuxPCSelect = 1  # not ra
        # MuxMASelect = 1     #PC send to MAR in step1
        MemRead = False
        MemWrite = False
    elif opcode == 99:  # SB type
        ALUOp = 1
        MuxBSelect = 0  # rs2 is required, imm is used in IAG
        MuxYSelect = 2  # ra, but don't-care
        BytestoRead = 0
        BytestoWrite = 0
        RegWrite = 0  # do not update register
        MuxINCSelect = 0  # to be updated after ALU
        MuxASelect = 0  # rs1
        branch = 1  # required to update control for branch inst
        MuxPCSelect = 1  # not ra
        # MuxMASelect = 1     #PC send to MAR in step1
        MemRead = False
        MemWrite = False

    ######mem#########
    # def InitMemory(self,PC_INST): # loads instruction to memory before execution of program
    #     for addr in PC_INST: # loop over every instruction
    #         for _byte in range(4): # loop over every byte in the instruction, extract it and store it in little-endian format
    #             byte=PC_INST[addr]&0x000000ff # bitmask to extract LS byte
    #             self.memory[addr+_byte]=byte
    #             PC_INST[addr]=PC_INST[addr]>>8 # bitwise right shift
    #     print("Program loaded to memory successfully")

    # def LoadInstruction(self,PC):
    #     if PC%4!=0: # PC must always be a multiple of 4, word alignment!
    #         print("Instruction not word aligned")
    #         sys.exit()
    #     elif PC<self.MIN_UNSIGNED_NUM or PC>self.MAX_PC: # PC should be in a valid range
    #         print("PC out of range!!")
    #     instruction=0 #stores instruction
    #     for _byte in range(4):
    #         instruction+=self.memory.get(PC+_byte,0)*(256**_byte)
    #     self.IRout=instruction
    #     self.MDR=instruction
    #     return instruction

    # # If MEM_read==true, ReadMemory is called.
    # # If MEM_write==true, then WriteMemory is called.
    # # Else, no action
    # def AccessMemory(self, MEM_read, MEM_write, base_address, byte_size, RMin):
    #     if MEM_read==1 and MEM_write==0:
    #         self.ReadMemory(base_address,byte_size)
    #     elif MEM_write==1 and MEM_read==0:
    #         self.WriteMemory(base_address,byte_size,RMin)
    #     elif MEM_read==0 and MEM_write==0:
    #         self.MDR=0
    #     elif MEM_read==1 and MEM_write==1: # may change in pipelining
    #         print("Invalid control signal received")
    #         sys.exit()
    #     return self.MDR


    # def ReadMemory(self, base_address, byte_size):
    #     self.MAR = base_address
    #     temp_mdr = 0
    #     for _byte in range(
    #             byte_size):  # different number of bytes need to be accessed based on the command, ld , lw etc.
    #         if base_address + _byte < self.MIN_SIGNED_NUM or base_address + _byte > self.MAX_SIGNED_NUM:  # check if the address lies in range of data segment or not
    #             print("Address is not in range of data segment")
    #             sys.exit()
    #         temp_data = self.memory.get(base_address + _byte, 0)  # accessing the data at BaseAddress + Byte
    #         for shift in range(_byte):  # for shifting left because of the little endian notation
    #             temp_data = temp_data << 8  # shifting by a byte or 8 bits
    #         temp_mdr += temp_data  # writing the shifted data to temp_mdr (note that if we are at base_address + 3 , then the data is shifted 3 times 8 bits at a time and then added to temp_mdr)
    #     self.MDR = temp_mdr  # writing the data extracted from memory to MDR

    # def WriteMemory(self, base_address, byte_size, RMin):   # writes data in RMin to address given by base_address
    #     self.MAR = base_address # MAR contains the base address to be written to
    #     self.MDR = RMin # MDR contains data to be written at address given by MAR
    #     for _byte in range(byte_size):  # loop over number of bytes to be written, data is written in little endian format
    #         byte = RMin&0x000000ff  # extract LSB
    #         if base_address+_byte < self.MIN_SIGNED_NUM or base_address+_byte > self.MAX_SIGNED_NUM: # check if the address lies in range of data segment or not
    #             print("Address is not in range of data segment")
    #             sys.exit()
    #         self.memory[base_address+_byte] = byte
    #         print("Address: "+hex(base_address+_byte) + " Data: " + hex(byte))
    #         RMin = RMin>>8 # shift right by 8 bits to set second last byte as LSB
    #     print("Memory write successful")

# a=ByteAddressableMemory()
# a.init_memory({0x4 :0x5a583,0x8 :0x300293})
# for key in a.memory:
#     print(hex(key),hex(a.memory[key]))

#######decoder#########
    # def Interpret_UJ(self):
    #     self.MemRead = False #Mem is not Read in jal
    #     self.MemWrite = False #mem is not written to in jal
    #     self.ALUop = 0  #ALU is not used in jal
    #     self.RegWrite = 1 #PC value is written to register
    #     self.IRwrite = 0
    #     self.PCwrite = 1 # PC has to be updated in Jump
    #     self.BytesToRead = 0 #don't care
    #     self.BytesToWrite = 0 #don't care
    #     self.MuxINCSelect = 1 #Branch offset in used in IAG instead of 4
    #     self.MuxPCSelect = 1 #PC is selected instead of base address
    #     self.MuxYSelect = 2 #ra given to MuxY
    #     self.branch = 0
    #     self.jump = 1
    #     self.MuxBSelect = 0 # don't cares
    #     self.MuxMASelect = 0 # don't cares
    #     self.MuxMDRSelect = 0 # don't cares

    # def Interpret_U(self):
    #     if self.opcode == 23:
    #     # print("auipc")
    #         self.MemRead = False #no memory read/write
    #         self.MemWrite = False
    #         self.ALUop = 1 #ALU is used to add to PC
    #         self.RegWrite = 1 #Register is updated
    #         self.IRwrite = 0
    #         self.PCwrite = 0
    #         self.BytesToRead = 0 # no memory access
    #         self.BytesToWrite = 0 # no memory access
    #         self.MuxINCSelect = 0 # 4 is chosen
    #         self.MuxPCSelect = 0 # PC is chosen, move sequentially next PC
    #         self.MuxYSelect = 0 # ALU output is chosen
    #         self.branch = 0
    #         self.jump = 0
    #         self.MuxBSelect = 1 # immediate selected
    #         self.MuxMASelect = 0 # don't care
    #         self.MuxMDRSelect = 0 # don't care
    #     elif self.opcode == 55:
    #     # print("lui")
    #         self.MemRead = False #no memory access
    #         self.MemWrite = False #no memory access
    #         self.ALUop = 1 # AlU is used
    #         self.RegWrite = 1 # Register is written to
    #         self.IRwrite = 0
    #         self.PCwrite = 0
    #         self.BytesToRead = 0 #don't care
    #         self.BytesToWrite = 0 #don't care
    #         self.MuxINCSelect = 0 #4 is added to PC
    #         self.MuxPCSelect = 1 # Pc is chosen
    #         self.MuxYSelect = 0 # ALU output is chosen
    #         self.branch = 0
    #         self.jump = 0
    #         self.MuxBSelect = 1 #imm is chosen
    #         self.MuxMASelect = 0 #don't care
    #         self.MuxMDRSelect = 0 #don't care

    # def Interpret_S(self):
    #     if self.funct3 == 0:
    #     # print("sb")
    #         self.MemRead = False
    #         self.MemWrite = True #Mem is written to
    #         self.ALUop = 1 #ALU is used to get address
    #         self.RegWrite = 0 #Register is not written to
    #         self.IRwrite = 0
    #         self.PCwrite = 0
    #         self.BytesToRead = 0 #don't care
    #         self.BytesToWrite = 1
    #         self.MuxINCSelect = 0
    #         self.MuxPCSelect = 1
    #         self.MuxYSelect = 0
    #         self.branch = 0
    #         self.jump = 0
    #         self.MuxBSelect = 1 #imm is used
    #         self.MuxMASelect = 0 #rz is used
    #         self.MuxMDRSelect = 0 #not sure
    #     elif self.funct3 == 1:
    #     # print("sh")
    #         self.MemRead = False
    #         self.MemWrite = True  # Mem is written to
    #         self.ALUop = 1  # ALU is used to get address
    #         self.RegWrite = 0  # Register is not written to
    #         self.IRwrite = 0
    #         self.PCwrite = 0
    #         self.BytesToRead = 0  # don't care
    #         self.BytesToWrite = 2
    #         self.MuxINCSelect = 0
    #         self.MuxPCSelect = 1
    #         self.MuxYSelect = 0
    #         self.branch = 0
    #         self.jump = 0
    #         self.MuxBSelect = 1  # imm is used
    #         self.MuxMASelect = 0  # rz is used
    #         self.MuxMDRSelect = 0  # not sure
    #     elif self.funct3 == 2:
    #         self.MemRead = False
    #         self.MemWrite = True  # Mem is written to
    #         self.ALUop = 1  # ALU is used to get address
    #         self.RegWrite = 0  # Register is not written to
    #         self.IRwrite = 0
    #         self.PCwrite = 0
    #         self.BytesToRead = 0  # don't care
    #         self.BytesToWrite = 4
    #         self.MuxINCSelect = 0
    #         self.MuxPCSelect = 1
    #         self.MuxYSelect = 0
    #         self.branch = 0
    #         self.jump = 0
    #         self.MuxBSelect = 1  # imm is used
    #         self.MuxMASelect = 0  # rz is used
    #         self.MuxMDRSelect = 0  # not sure

    # # print("sw")

    # def Interpret_SB(self):
    #     if self.funct3 == 0:
    #     # print("beq")
    #     elif self.funct3 == 1:
    #     # print("bne")
    #     elif self.funct3 == 4:
    #     # print("blt")
    #     elif self.funct3 == 5:

    # # print("bge")

    # def Interpret_I(self):
    #     if self.opcode == 19:
    #         if self.funct3 == 0:
    #         # print("addi")
    #             self.MemRead = False
    #             self.MemWrite = False
    #             self.ALUop = 1
    #             self.RegWrite = 1
    #             self.IRwrite = 0
    #             self.PCwrite = 0
    #             self.BytesToRead = 0
    #             self.BytesToWrite = 0
    #             self.MuxINCSelect = 0
    #             self.MuxPCSelect = 1
    #             self.MuxYSelect = 0
    #             self.branch = 0
    #             self.jump = 0
    #             self.MuxBSelect = 1
    #             self.MuxMASelect = 0
    #             self.MuxMDRSelect = 0
    #         elif self.funct3 == 7:
    #         # print("andi")
    #             self.MemRead = False
    #             self.MemWrite = False
    #             self.ALUop = 1
    #             self.RegWrite = 1
    #             self.IRwrite = 0
    #             self.PCwrite = 0
    #             self.BytesToRead = 0
    #             self.BytesToWrite = 0
    #             self.MuxINCSelect = 0
    #             self.MuxPCSelect = 1
    #             self.MuxYSelect = 0
    #             self.branch = 0
    #             self.jump = 0
    #             self.MuxBSelect = 1
    #             self.MuxMASelect = 0
    #             self.MuxMDRSelect = 0
    #         elif self.funct3 == 6:
    #         # print("ori")
    #             self.MemRead = False
    #             self.MemWrite = False
    #             self.ALUop = 1
    #             self.RegWrite = 1
    #             self.IRwrite = 0
    #             self.PCwrite = 0
    #             self.BytesToRead = 0
    #             self.BytesToWrite = 0
    #             self.MuxINCSelect = 0
    #             self.MuxPCSelect = 1
    #             self.MuxYSelect = 0
    #             self.branch = 0
    #             self.jump = 0
    #             self.MuxBSelect = 1
    #             self.MuxMASelect = 0
    #             self.MuxMDRSelect = 0
    #     elif self.opcode == 3:
    #         if self.funct3 == 0:
    #         # print("lb")
    #             self.MemRead = False
    #             self.MemWrite = False
    #             self.ALUop = 1
    #             self.RegWrite = 1
    #             self.IRwrite = 0
    #             self.PCwrite = 0
    #             self.BytesToRead = 0
    #             self.BytesToWrite = 0
    #             self.MuxINCSelect = 0
    #             self.MuxPCSelect = 0
    #             self.MuxYSelect = 0
    #             self.branch = 0
    #             self.jump = 0
    #             self.MuxBSelect = 1
    #             self.MuxMASelect = 0
    #             self.MuxMDRSelect = 0
    #         elif self.funct3 == 1:
    #         # print("lh")
    #             self.MemRead = False
    #             self.MemWrite = False
    #             self.ALUop = 1
    #             self.RegWrite = 1
    #             self.IRwrite = 0
    #             self.PCwrite = 0
    #             self.BytesToRead = 0
    #             self.BytesToWrite = 0
    #             self.MuxINCSelect = 0
    #             self.MuxPCSelect = 0
    #             self.MuxYSelect = 0
    #             self.branch = 0
    #             self.jump = 0
    #             self.MuxBSelect = 1
    #             self.MuxMASelect = 0
    #             self.MuxMDRSelect = 0
    #         elif self.funct3 == 2:
    #         # print("lw")
    #             self.MemRead = False
    #             self.MemWrite = False
    #             self.ALUop = 1
    #             self.RegWrite = 1
    #             self.IRwrite = 0
    #             self.PCwrite = 0
    #             self.BytesToRead = 0
    #             self.BytesToWrite = 0
    #             self.MuxINCSelect = 0
    #             self.MuxPCSelect = 0
    #             self.MuxYSelect = 0
    #             self.branch = 0
    #             self.jump = 0
    #             self.MuxBSelect = 0
    #             self.MuxMASelect = 0
    #             self.MuxMDRSelect = 0
    #     elif self.opcode == 103:
    #     # print("jalr")
    #         self.MemRead = False
    #         self.MemWrite = False
    #         self.ALUop = 1
    #         self.RegWrite = 1
    #         self.IRwrite = 0
    #         self.PCwrite = 0
    #         self.BytesToRead = 0
    #         self.BytesToWrite = 0
    #         self.MuxINCSelect = 0
    #         self.MuxPCSelect = 0
    #         self.MuxYSelect = 0
    #         self.branch = 0
    #         self.jump = 0
    #         self.MuxBSelect = 0
    #         self.MuxMASelect = 0
    #         self.MuxMDRSelect = 0

    # def Interpret_R(self):
    #     if self.funct3 == 0 and self.funct7 == 0:
    #         #print("add")
    #         self.MemRead = False
    #         self.MemWrite = False
    #         self.ALUop = 1
    #         self.RegWrite = 1
    #         self.IRwrite = 0
    #         self.PCwrite = 0
    #         self.BytesToRead = 0
    #         self.BytesToWrite = 0
    #         self.MuxINCSelect = 0
    #         self.MuxPCSelect = 0
    #         self.MuxYSelect = 0
    #         self.branch= 0
    #         self.jump = 0
    #         self.MuxBSelect = 0
    #         self.MuxMASelect = 0
    #         self.MuxMDRSelect = 0

    #     elif self.funct3 == 7 and self.funct7 == 0:
    #         # print("and")
    #         self.MemRead = False
    #         self.MemWrite = False
    #         self.ALUop = 1
    #         self.RegWrite = 1
    #         self.IRwrite = 0
    #         self.PCwrite = 0
    #         self.BytesToRead = 0
    #         self.BytesToWrite = 0
    #         self.MuxINCSelect = 0
    #         self.MuxPCSelect = 0
    #         self.MuxYSelect = 0
    #         self.branch = 0
    #         self.jump = 0
    #         self.MuxBSelect = 0
    #         self.MuxMASelect = 0
    #         self.MuxMDRSelect = 0

    #     elif self.funct3 == 6 and self.funct7 == 0:
    #         # print("or")
    #         self.MemRead = False
    #         self.MemWrite = False
    #         self.ALUop = 1
    #         self.RegWrite = 1
    #         self.IRwrite = 0
    #         self.PCwrite = 0
    #         self.BytesToRead = 0
    #         self.BytesToWrite = 0
    #         self.MuxINCSelect = 0
    #         self.MuxPCSelect = 0
    #         self.MuxYSelect = 0
    #         self.branch = 0
    #         self.jump = 0
    #         self.MuxBSelect = 0
    #         self.MuxMASelect = 0
    #         self.MuxMDRSelect = 0

    #     elif self.funct3 == 1 and self.funct7 == 0:
    #         # print("sll")
    #         self.MemRead = False
    #         self.MemWrite = False
    #         self.ALUop = 1
    #         self.RegWrite = 1
    #         self.IRwrite = 0
    #         self.PCwrite = 0
    #         self.BytesToRead = 0
    #         self.BytesToWrite = 0
    #         self.MuxINCSelect = 0
    #         self.MuxPCSelect = 0
    #         self.MuxYSelect = 0
    #         self.branch = 0
    #         self.jump = 0
    #         self.MuxBSelect = 0
    #         self.MuxMASelect = 0
    #         self.MuxMDRSelect = 0

    #     elif self.funct3 == 2 and self.funct7 == 0:
    #         # print("slt")
    #         self.MemRead = False
    #         self.MemWrite = False
    #         self.ALUop = 1
    #         self.RegWrite = 1
    #         self.IRwrite = 0
    #         self.PCwrite = 0
    #         self.BytesToRead = 0
    #         self.BytesToWrite = 0
    #         self.MuxINCSelect = 0
    #         self.MuxPCSelect = 0
    #         self.MuxYSelect = 0
    #         self.branch = 0
    #         self.jump = 0
    #         self.MuxBSelect = 0
    #         self.MuxMASelect = 0
    #         self.MuxMDRSelect = 0

    #     elif self.funct3 == 5 and self.funct7 == 32:
    #         # print("sra")
    #         self.MemRead = False
    #         self.MemWrite = False
    #         self.ALUop = 1
    #         self.RegWrite = 1
    #         self.IRwrite = 0
    #         self.PCwrite = 0
    #         self.BytesToRead = 0
    #         self.BytesToWrite = 0
    #         self.MuxINCSelect = 0
    #         self.MuxPCSelect = 0
    #         self.MuxYSelect = 0
    #         self.branch = 0
    #         self.jump = 0
    #         self.MuxBSelect = 0
    #         self.MuxMASelect = 0
    #         self.MuxMDRSelect = 0
    #     elif self.funct3 == 5 and self.funct7 == 0:
    #         # print("srl")
    #         self.MemRead = False
    #         self.MemWrite = False
    #         self.ALUop = 1
    #         self.RegWrite = 1
    #         self.IRwrite = 0
    #         self.PCwrite = 0
    #         self.BytesToRead = 0
    #         self.BytesToWrite = 0
    #         self.MuxINCSelect = 0
    #         self.MuxPCSelect = 0
    #         self.MuxYSelect = 0
    #         self.branch = 0
    #         self.jump = 0
    #         self.MuxBSelect = 0
    #         self.MuxMASelect = 0
    #         self.MuxMDRSelect = 0
    #     elif self.funct3 == 0 and self.funct7 == 32:
    #         # print("sub")
    #         self.MemRead = False
    #         self.MemWrite = False
    #         self.ALUop = 1
    #         self.RegWrite = 1
    #         self.IRwrite = 0
    #         self.PCwrite = 0
    #         self.BytesToRead = 0
    #         self.BytesToWrite = 0
    #         self.MuxINCSelect = 0
    #         self.MuxPCSelect = 0
    #         self.MuxYSelect = 0
    #         self.branch = 0
    #         self.jump = 0
    #         self.MuxBSelect = 0
    #         self.MuxMASelect = 0
    #         self.MuxMDRSelect = 0
    #     elif self.funct3 == 4 and self.funct7 == 0:
    #         # print("xor")
    #         self.MemRead = False
    #         self.MemWrite = False
    #         self.ALUop = 1
    #         self.RegWrite = 1
    #         self.IRwrite = 0
    #         self.PCwrite = 0
    #         self.BytesToRead = 0
    #         self.BytesToWrite = 0
    #         self.MuxINCSelect = 0
    #         self.MuxPCSelect = 0
    #         self.MuxYSelect = 0
    #         self.branch = 0
    #         self.jump = 0
    #         self.MuxBSelect = 0
    #         self.MuxMASelect = 0
    #         self.MuxMDRSelect = 0
    #     elif self.funct3 == 0 and self.funct7 == 1:
    #         # print("mul")
    #         self.MemRead = False
    #         self.MemWrite = False
    #         self.ALUop = 1
    #         self.RegWrite = 1
    #         self.IRwrite = 0
    #         self.PCwrite = 0
    #         self.BytesToRead = 0
    #         self.BytesToWrite = 0
    #         self.MuxINCSelect = 0
    #         self.MuxPCSelect = 0
    #         self.MuxYSelect = 0
    #         self.branch = 0
    #         self.jump = 0
    #         self.MuxBSelect = 0
    #         self.MuxMASelect = 0
    #         self.MuxMDRSelect = 0
    #     elif self.funct3 == 4 and self.funct7 == 1:
    #         # print("div")
    #         self.MemRead = False
    #         self.MemWrite = False
    #         self.ALUop = 1
    #         self.RegWrite = 1
    #         self.IRwrite = 0
    #         self.PCwrite = 0
    #         self.BytesToRead = 0
    #         self.BytesToWrite = 0
    #         self.MuxINCSelect = 0
    #         self.MuxPCSelect = 0
    #         self.MuxYSelect = 0
    #         self.branch = 0
    #         self.jump = 0
    #         self.MuxBSelect = 0
    #         self.MuxMASelect = 0
    #         self.MuxMDRSelect = 0
    #     elif self.funct3 == 6 and self.funct7 == 1:
    #         # print("rem")
    #         self.MemRead = False
    #         self.MemWrite = False
    #         self.ALUop = 1
    #         self.RegWrite = 1
    #         self.IRwrite = 0
    #         self.PCwrite = 0
    #         self.BytesToRead = 0
    #         self.BytesToWrite = 0
    #         self.MuxINCSelect = 0
    #         self.MuxPCSelect = 0
    #         self.MuxYSelect = 0
    #         self.branch = 0
    #         self.jump = 0
    #         self.MuxBSelect = 0
    #         self.MuxMASelect = 0
    #         self.MuxMDRSelect = 0

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
