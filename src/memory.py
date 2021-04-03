#!/usr/bin/python3
# code for memory module. We will most probably be using hashes for memory
import sys

class ByteAddressableMemory:
    MAX_SIGNED_NUM=0x7fffffff
    MIN_SIGNED_NUM=0x10000000
    MAX_UNSIGNED_NUM=0xffffffff
    MIN_UNSIGNED_NUM=0x00000000
    MAX_PC=0x7ffffffc

    def __init__(self):
        self.memory=dict() # key as address, value as memory content. Memory byte addressable! Thus, every element stores a byte
        self.MAR=0 # Memory address register
        self.MDR=0
        self.IRout=0

    def InitMemory(self,PC_INST): # loads instruction to memory before execution of program
        for addr in PC_INST: # loop over every instruction
            for _byte in range(4): # loop over every byte in the instruction, extract it and store it in little-endian format
                byte=PC_INST[addr]&0x000000ff # bitmask to extract LS byte
                self.memory[addr+_byte]=byte
                PC_INST[addr]=PC_INST[addr]>>8 # bitwise right shift
        print("Program loaded to memory successfully")

    def LoadInstruction(self,PC):
        if PC%4!=0: # PC must always be a multiple of 4, word alignment!
            print("Instruction not word aligned")
            sys.exit()
        elif PC<self.MIN_UNSIGNED_NUM or PC>self.MAX_PC: # PC should be in a valid range
            print("PC out of range!!")
        instruction=0 #stores instruction
        for _byte in range(4):
            instruction+=self.memory.get(PC+_byte,0)*(256**_byte)
        self.IRout=instruction
        self.MDR=instruction
        return instruction

    def AccessMemory(self,control):

    def ReadMemory(self, base_address, byte_size):
        self.MAR = base_address
        temp_mdr = 0
        for _byte in range(
                byte_size):  # different number of bytes need to be accessed based on the command, ld , lw etc.
            if base_address + _byte < self.MIN_SIGNED_NUM or base_address + _byte > self.MAX_SIGNED_NUM:  # check if the address lies in range of data segment or not
                print("Address is not in range of data segment")
                sys.exit()
            temp_data = self.memory.get(base_address + _byte, 0)  # accessing the data at BaseAddress + Byte
            for shift in range(_byte):  # for shifting left because of the little endian notation
                temp_data = temp_data << 8  # shifting by a byte or 8 bits
            temp_mdr + temp_data  # writing the shifted data to temp_mdr (note that if we are at base_address + 3 , then the data is shifted 3 times 8 bits at a time and then added to temp_mdr)
        self.MDR = temp_mdr  # writing the data extracted from memory to MDR

    def WriteMemory(self, base_address, byte_size, RMin):   # writes data in RMin to address given by base_address
        self.MAR = base_address # MAR contains the base address to be written to
        self.MDR = RMin # MDR contains data to be written at address given by MAR
        for _byte in range(byte_size):  # loop over number of bytes to be written, data is written in little endian format
            byte = RMin&0x000000ff  # extract LSB
            if base_address+_byte < self.MIN_SIGNED_NUM or base_address+_byte > self.MAX_SIGNED_NUM: # check if the address lies in range of data segment or not
                print("Address is not in range of data segment")
                sys.exit()
            self.memory[base_address+_byte] = byte
            print("Address: "+hex(base_address+_byte) + " Data: " + hex(byte))
            RMin = RMin>>8 # shift right by 8 bits to set second last byte as LSB
        print("Memory write successful")

# a=ByteAddressableMemory()
# a.init_memory({0x4 :0x5a583,0x8 :0x300293})
# for key in a.memory:
#     print(hex(key),hex(a.memory[key]))
