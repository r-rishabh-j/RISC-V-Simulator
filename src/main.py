# !/usr/bin/python3
import MachineCodeParser # import parser for parsing machine code into PC and corresponding instructions.
import RiscSim
#import memory
MachineCodeParser.parser("instructions.mc") # supply input file name
# for key in MachineCodeParser.PC_INST:
#     print(hex(key),hex(MachineCodeParser.PC_INST[key]))

#program load
RiscSim.memory.InitMemory(MachineCodeParser.PC_INST)
#Run the simulator
RiscSim.RunSim()

####################################################file dumping############################################################
#fileReg=open("RegisterDump.mc",'w')
#fileMem=open("MemoryDump.mc",'w')

def padhexa(s):
    return '0x' + s[2:].zfill(8)

#def print_reg(arr):  # input is numpy array
with open(f"RegisterDump.mc", "w") as fileReg:
    for i in range(32):
        fileReg.write(f"x{i} ")  # print address of register for eg. x5
        if (RiscSim.registers.reg[i] >= 0):
            fileReg.write(padhexa(hex(RiscSim.registers.reg[i])))
        else:
            reg = RiscSim.registers.reg[i] & 0xffffffff  # signed
            fileReg.write(hex(reg))
        fileReg.write("\n")

# dumping memory
with open(f"MemoryDump.mc", "w") as fileMem:  # input is dictionary with key as address and value as data
    lst = []  # stores keys present in dictionary
    temp_lst = []  # stores base address
    for key in RiscSim.memory.memory_module.memory:
        lst.append(key)
    lst.sort()
    for x in lst:
        temp = x - (x % 4)  # storing base address in temp
        if temp not in temp_lst:  # if base address not present in temp_list , then append it
            temp_lst.append(temp)
    temp_lst.sort()
    for i in temp_lst:
        fileMem.write(f"{padhexa(hex(i))} ")  # printing base address
        if i in lst:
            fileMem.write(f"{padhexa(hex(RiscSim.memory.memory_module.memory[i]))[8:]} " )  # if data in dictionary
        else:
            fileMem.write("00  ")  # if data not in dictionary
        if (i + 1) in lst:
            fileMem.write(f"{padhexa(hex(RiscSim.memory.memory_module.memory[i + 1]))[8:]} ")
        else:
            fileMem.write("00  ")
        if (i + 2) in lst:
            fileMem.write(f"{padhexa(hex(RiscSim.memory.memory_module.memory[i + 2]))[8:]} ")
        else:
            fileMem.write("00  ")
        if (i + 3) in lst:
            fileMem.write(f"{padhexa(hex(RiscSim.memory.memory_module.memory[i + 3]))[8:]} ")
        else:
            fileMem.write("00  ")
        fileMem.write("\n")  # new line
print("Files dump successfully")
