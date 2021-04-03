#!/usr/bin/python3
# code for memory module. We will most probably be using hashes for memory
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

    def WriteMemory(self):
# a=ByteAddressableMemory()
# a.init_memory({0x4 :0x5a583,0x8 :0x300293})
# for key in a.memory:
#     print(hex(key),hex(a.memory[key]))