#!/usr/bin/python3
# code for memory module. We will most probably be using hashes for memory
import sys

class ByteAddressableMemory:
    MAX_SIGNED_NUM=0x7fffffff
    MIN_SIGNED_NUM=0x10000000
    MAX_UNSIGNED_NUM=0xffffffff
    MIN_UNSIGNED_NUM=0x00000000

    def __init__(self):
        self.memory=dict() # key as address, value as memory content. Memory byte addressable! Thus, every element stores a byte
        self.MAR=0
        self.MDR=0
        self.IRout=0

    def InitMemory(self,PC_INST): # loads instruction to memory before execution of program
        for addr in PC_INST: # loop over every instruction
            for _byte in range(4): # loop over every byte in the instruction, extract it and store it in little-endian format
                byte=PC_INST[addr]&0x000000ff # bitmask to extract LS byte
                self.memory[addr+_byte]=byte
                PC_INST[addr]=PC_INST[addr]>>8 # bitwise right shift
        print("Program loaded to memory successfully")

    def AccessMemory(self,control):

    def ReadMemory(self):

    def WriteMemory(self, base_address, byte_size, RMin):   # writes data in RMin to address given by base_address
        self.MAR = base_address # MAR contains the base address to be written to
        self.MDR = RMin # MDR contains data to be written at address given by MAR
        for _byte in range(byte_size):  # loop over number of bytes to be written, data is written in little endian format
            byte = RMin&0x000000ff  # extract LSB
            if base_address+_byte < self.MIN_SIGNED_NUM or base_address+_byte > self.MAX_SIGNED_NUM: # check if the address lies in range of data segment or not
                print("Address is not in range of data segment")
                sys.exit()
            self.memory[base_address+_byte] = byte
            print("Address: "+hex(base_address+byte) + " Data: " + hex(byte))
            RMin = RMin>>8 # shift right by 8 bits to set second last byte as LSB
        print("Memory write successful")

# a=ByteAddressableMemory()
# a.init_memory({0x4 :0x5a583,0x8 :0x300293})
# for key in a.memory:
#     print(hex(key),hex(a.memory[key]))
