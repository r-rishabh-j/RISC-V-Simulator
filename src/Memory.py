#!/usr/bin/python3
# code for memory module. We will most probably be using hashes for memory
import sys

class ProcessorMemoryInterface:
    def __init__(self):
        self.MAR=0 # Memory address register
        self.MDR=0
        self.IRout=0
        self.memory_module=ByteAddressableMemory()

    def InitMemory(self,PC_INST): # loads instruction to memory before execution of program
        for addr in PC_INST: # loop over every instruction
            self.memory_module.WriteValueAtAddress(addr,4,PC_INST[addr])
        print("Program loaded to memory successfully")

    def LoadInstruction(self,PC):
        if PC%4!=0: # PC must always be a multiple of 4, word alignment!
            raise Exception("Instruction not word aligned")
        elif PC<self.MIN_UNSIGNED_NUM or PC>self.MAX_PC: # PC should be in a valid range
            raise Exception("PC out of range!!")
        self.MAR=PC
        instruction=0 #stores instruction
        instruction=self.memory_module.GetUnsignedValueAtAddress(self.MAR,4)
        self.IRout=instruction
        self.MDR=instruction
        print(f"Loaded instruction from {hex(PC)}")
        return instruction

    # If MEM_read==true, ReadMemory is called.
    # If MEM_write==true, then WriteMemory is called.
    # Else, no action
    def AccessMemory(self, MEM_read :bool, MEM_write :bool, base_address :int, byte_size :int, RMin: int):
        if MEM_read==1 and MEM_write==0:
            self.ReadMemory(base_address,byte_size)
        elif MEM_write==1 and MEM_read==0:
            self.WriteMemory(base_address,byte_size,RMin)
        elif MEM_read==0 and MEM_write==0:
            self.MDR=0
        elif MEM_read==1 and MEM_write==1: # may change in pipelining
            raise Exception("Invalid control signal received")
        return self.MDR


    def ReadMemory(self, base_address:int, no_of_bytes:int):
        self.MAR = base_address
        self.MDR=self.memory_module.GetSignedValueAtAddress(self.MAR, no_of_bytes)
        print(f"Read {no_of_bytes} bytes from {hex(base_address)}")
        data=self.MDR
        return data

    def WriteMemory(self, base_address:int, byte_size:int, RMin:int):   # writes data in RMin to address given by base_address
        self.MAR = base_address # MAR contains the base address to be written to
        self.MDR = RMin # MDR contains data to be written at address given by MAR
        self.memory_module.WriteValueAtAddress(base_address, byte_size, self.MDR)
        print(f"Wrote {byte_size} bytes at {hex(base_address)}")

class ByteAddressableMemory:
    MAX_SIGNED_NUM=0x7fffffff
    MIN_SIGNED_NUM=-0x80000000
    MAX_UNSIGNED_NUM=0xffffffff
    MIN_UNSIGNED_NUM=0x00000000
    MAX_PC=0x7ffffffc

    def __init__(self):
        self.memory=dict() # key as address, value as memory content. Memory byte addressable! Thus, every element stores a byte
        
    def GetUnsignedValueAtAddress(self, base_address : int, no_of_bytes: int):
        data=0
        for _byte in range(no_of_bytes):
            if base_address + _byte < self.MIN_UNSIGNED_NUM or base_address + _byte > self.MAX_SIGNED_NUM:  # check if the address lies in range of data segment or not
                raise Exception("Address is not in range of data segment")
            data+=self.memory.get(base_address+_byte,0)*(256**_byte)
        return data

    def GetSignedValueAtAddress(self, base_address : int, no_of_bytes: int):
        if(no_of_bytes==3):
            raise Exception("Instruction not supported")
        data=0
        for _byte in range(no_of_bytes):  # different number of bytes need to be accessed based on the command, ld , lw etc.
            if base_address + _byte < self.MIN_UNSIGNED_NUM or base_address + _byte > self.MAX_SIGNED_NUM:  # check if the address lies in range of data segment or not
                raise Exception("Address is not in range of data segment")
            data+=self.memory.get(base_address+_byte,0)*(256**_byte)
        # conversion to signed value
        MSmask=0 # to get MSB
        unsigned_num_mask=0 # to get all bits except MSB
        if(no_of_bytes==1):
            MSmask=0x80
            unsigned_num_mask=0x7f
        elif(no_of_bytes==2):
            MSmask=0x8000
            unsigned_num_mask=0x7fff
        elif(no_of_bytes==4):
            MSmask=0x80000000
            unsigned_num_mask=0x7fffffff
        data=(-(data&MSmask)+(data&unsigned_num_mask))
        return data

    def WriteValueAtAddress(self, base_address : int, no_of_bytes: int, write_val: int): # can take both signed/unsigned value
        for _byte in range(no_of_bytes): # loop over every byte in the instruction, extract it and store it in little-endian format
            byte=write_val&0x000000ff # bitmask to extract LS byte
            if base_address+_byte>self.MAX_SIGNED_NUM or base_address+_byte<self.MIN_UNSIGNED_NUM:
                raise Exception("Memory address out of range! Segmentation fault(core dumped)")
            self.memory[base_address+_byte]=byte
            write_val=write_val>>8 # bitwise right shift


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
