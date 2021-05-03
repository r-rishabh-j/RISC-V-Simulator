#!/usr/bin/python3
# code for memory module. We will most probably be using hashes for memory
import sys

class ProcessorMemoryInterface: # the main PMI
    MAX_SIGNED_NUM = 0x7fffffff
    MIN_SIGNED_NUM = -0x80000000
    MAX_UNSIGNED_NUM = 0xffffffff
    MIN_UNSIGNED_NUM = 0x00000000
    MAX_PC = 0x7ffffffc
    def __init__(self, cache_associativity, cache_size, cache_block_size):
        self.MAR=0 # Memory address register
        self.MAR_pc=0
        self.MDR=0
        self.IRout=0
        self.take_from_rm=False
        self.text_module=TwoLevelMemory(cache_associativity, cache_size, cache_block_size) # contains I$
        self.data_module=TwoLevelMemory(cache_associativity, cache_size, cache_block_size) # contains D$
        
    def InitMemory(self,PC_INST,DATA): # loads instruction to memory before execution of program
        for addr in PC_INST: # loop over every instruction
            self.text_module.WriteValueAtAddress(addr,4,PC_INST[addr])
        for addr in DATA: # loop over every data load
            self.data_module.WriteValueAtAddress(addr,4,DATA[addr])
        print("\033[92mProgram and data loaded to memory successfully\033[0m")

    def LoadInstruction(self,PC):
        if PC%4!=0: # PC must always be a multiple of 4, word alignment!
            raise Exception("\033[1;31mInstruction not word aligned\033[0m")
        elif PC<self.MIN_UNSIGNED_NUM or PC>self.MAX_PC: # PC should be in a valid range
            raise Exception("\033[1;31mPC out of range!!\033[0m")
        self.MAR_pc=PC
        instruction=0 #stores instruction
        instruction=self.text_module.GetUnsignedValueAtAddress(self.MAR_pc,4)
        self.IRout=instruction
        print(f"\033[93mLoaded instruction from {hex(PC)} {hex(instruction)}\033[0m")
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
            raise Exception("\033[1;31mInvalid control signal received\033[0m")
        return self.MDR


    def ReadMemory(self, base_address:int, no_of_bytes:int):
        self.MAR = base_address
        self.MDR=self.data_module.GetSignedValueAtAddress(self.MAR, no_of_bytes)
        print(f"\033[93mRead {no_of_bytes} bytes from {hex(base_address)}, value= {self.MDR}\033[0m")
        data=self.MDR
        return data

    def WriteMemory(self, base_address:int, byte_size:int, RMin:int):   # writes data in RMin to address given by base_address
        self.MAR = base_address # MAR contains the base address to be written to
        self.MDR = RMin # MDR contains data to be written at address given by MAR
        self.data_module.WriteValueAtAddress(base_address, byte_size, self.MDR)
        print(f"\033[93mWrote {byte_size} bytes at {hex(base_address)}, value={RMin}\033[0m")

# class CacheInterface: # interface between cache and TwoLevelMemory
#     def __init__(self, associativity, cache_size, block_size):
#         self._associativity=associativity
#         self._block_size=block_size
#         self._size=cache_size
#         self.cache_module=SetAssociativeCache(self._associativity, self._size, self._block_size)

class SetAssociativeCache: # cache module
    def __init__(self, associativity, cache_size, block_size):
        self._associativity=associativity
        self._block_size=block_size
        self._size=cache_size
        # visualize tag array in the form of a matrix(NxM), sets are the rows, set elements are along the column
        self.tag_array = [[-1 for j in range(associativity)] for i in range((cache_size//block_size)//associativity)] # blocks in the cache are indexed 0 through num-1
        self.set_array = [CacheSet(self.associativity,self.block_size) for i in range((cache_size//block_size)//associativity)] # contains the set objects
        # block element corresponds to a tag element in row major format, index=i*n+j, given tag is (i,j)
        
    def checkHit(self, tag, index): # returns boolean for found/not found
        isValid=False
        for block in self.tag_array[index]:
            if block!=-1:
                if tag==block:
                    return True
        return False
    
    def readDataFromCache(self, tag, index, block_offset, no_of_bytes):# return -1 if not found, else list of bytes
        # used for load instructions and for fetching instructions
        isHit=False
        block_index=0
        for block in self.tag_array[index]:
            if block!=-1:
                if tag==block:
                    isHit=True
                    block_index=block_index+1
                    break
        if not isHit:
            return -1
        return self.set_array[index].getDataFromBlock(block_index, block_offset, no_of_bytes) # returns a list
    
    def writeWhenNotHit(self, tag, index, block_offset, data: list, no_of_bytes):
        # to be called when read unsuccessful in the cache and now we have to allocate space in the cache for the data

    def writeDataToCache(self, tag, index, block_offset, data: list, no_of_bytes): # returns -1 if tag not found in cache, else returns 1 and writes data
        # to be called for store instructions only
        # takes a list of data containing each byte
        isHit=False
        block_index=0
        for block in self.tag_array[index]:
            if block!=-1:
                if tag==block:
                    isHit=True
                    block_index=block_index+1
                    break
        if not isHit: # tag not found
            return -1
        # tag found, now write data
        self.set_array[index].writeDataToBlock(block_index, block_offset, data, no_of_bytes)
        return 1



class CacheSet: # set object, contains LRU
    def __init__(self, associativity, block_size):
        self._associativity=associativity
        self._block_size=block_size
        self.blocks = [CacheBlock(self._block_size) for i in range(self._associativity)] #[[[] for j in range(associativity)] for i in range((cache_size//block_size)//associativity)]
    
    def getDataFromBlock(self, block_index, block_offset, no_of_bytes):
        return self.blocks[block_index].returnData(block_offset, no_of_bytes)
    
    def writeDataToBlock(self, block_index, block_offset, data: list, no_of_bytes):
        self.blocks[index].writeData(block_offset, data, no_of_bytes)

    def update_state_hit(self,index_up):  # contains the index of the block which was just updated
        temp=self.blocks[index_up].pref_count # now I will decrement the pref_count of all blocks whos pref_count is greater than temp
        for i in range(self._associativity):
            if self.blocks[i].valid == True:   # only updating if it is a valid cache block
                if self.blocks[i].pref_count>temp:    # only decrementing if the pref_count of this block is greater than the pref value of block which was just now accessed
                    self.blocks[i].pref_count=self.blocks[i].pref_count-1

        self.blocks[index_up].pref_count=self._associativity-1  # now this has the highers value since this was most recently accessed
            
class CacheBlock: # object for an individual cache block
    def __init__(self, block_size):
        self.size=block_size
        self.storage=[0 for byte in range(block_size)]
        self.pref_count=-1
        self.valid=False # boolean to check if the block contains any data
    
    def returnData(self, block_offset, no_of_bytes):
        data=[]
        for byte in range(no_of_bytes):
            if block_offset>=self.size:
                raise Exception("Data not word aligned!")
            data.append(self.storage[block_offset])
            block_offset+=1
        return data

    def writeData(self, block_offset, data: list, no_of_bytes):
        self.valid=True
        for byte in range(no_of_bytes):
            if block_offset>=self.size:
                raise Exception("Data not word aligned!")
            self.storage[block_offset]=data[byte]
            block_offset+=1
        return True
            

class TwoLevelMemory:
    MAX_SIGNED_NUM=0x7fffffff
    MIN_SIGNED_NUM=-0x80000000
    MAX_UNSIGNED_NUM=0xffffffff
    MIN_UNSIGNED_NUM=0x00000000
    MAX_PC=0x7ffffffc

    def __init__(self, cache_associativity, cache_size, cache_block_size):
        self.memory=dict() # key as address, value as memory content. Memory byte addressable! Thus, every element stores a byte
        if not isinstance(cache_size/block_size, int) or cache_size/block_size<1:
            raise Exception("Invalid selection of block and cache size!")
        if not isinstance((cache_size/block_size)/cache_associativity, int) or (cache_size/block_size)/cache_associativity<1:
            raise Exception("Invalid Selection of cache associativity!") 
        self.cache_module=SetAssociativeCache(cache_associativity, cache_size, cache_block_size)
        self.cache_size=cache_size
        self.cache_block_size=cache_block_size
        self.cache_associativity=cache_associativity
        self.cache_accesses=0
        self.cache_hits=0
        self.cache_miss=0

    def generateCacheAddress(self, base_address): # returns [tag, index, block_offset]
        tag=base_address-base_address%self.cache_block_size # tag is simply the base address of the block in memory
        index=(tag/self.cache_block_size)%self.cache_associativity # block number/associativity
        block_offset=base_address%self.cache_block_size
        return [tag, index, block_offset]

    def GetUnsignedValueAtAddress(self, base_address : int, no_of_bytes: int):
        data=0
        for _byte in range(no_of_bytes):
            if base_address + _byte < self.MIN_UNSIGNED_NUM or base_address + _byte > self.MAX_SIGNED_NUM:  # check if the address lies in range of data segment or not
                raise Exception("\033[1;31mAddress is not in range of data segment\033[0m")
            data+=self.memory.get(base_address+_byte,0)*(256**_byte)
        return data

    def GetSignedValueAtAddress(self, base_address : int, no_of_bytes: int):
        if(no_of_bytes==3):
            raise Exception("\033[1;31mInstruction not supported\033[0m")
        data=0
        for _byte in range(no_of_bytes):  # different number of bytes need to be accessed based on the command, ld , lw etc.
            if base_address + _byte < self.MIN_UNSIGNED_NUM or base_address + _byte > self.MAX_SIGNED_NUM:  # check if the address lies in range of data segment or not
                raise Exception("\033[1;31mAddress is not in range of data segment\033[0m")
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
        val=write_val
        for _byte in range(no_of_bytes): # loop over every byte in the instruction, extract it and store it in little-endian format
            byte=val&0x000000ff # bitmask to extract LS byte
            if base_address+_byte>self.MAX_SIGNED_NUM or base_address+_byte<self.MIN_UNSIGNED_NUM:
                raise Exception("\033[1;31mMemory address out of range! Segmentation fault(core dumped)\033[0m")
            self.memory[base_address+_byte]=byte
            val=val>>8 # bitwise right shift