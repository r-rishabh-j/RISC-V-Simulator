# !/usr/bin/python3
import MachineCodeParser # import parser for parsing machine code into PC and corresponding instructions.
import RunSim_forward
import sys
#import memory
if(len(sys.argv)==1):
    print("File name not supplied!")
    sys.exit()
MachineCodeParser.parser(sys.argv[1]) # supply input file name
# for key in MachineCodeParser.PC_INST:
#     print(hex(key),hex(MachineCodeParser.PC_INST[key]))

#program load
#Run the simulator
print_reg_file=int(input("Printing the register file at the end of each cycle, 1 for ON, 0 for OFF: "))
if print_reg_file not in [0,1]:
    print("Wrong knob")
    sys.exit()
print_buff_file=int(input("Printing the pipeline buffer at the end of each cycle, 1 for ON, 0 for OFF: "))
if print_reg_file not in [0,1]:
    print("Wrong knob")
    sys.exit()
# print_nth_buff=int(input("Specific instruction: 0 for off, instruction for on: "))
# if print_nth_buff<0:
#     print("Wrong knob")
#     sys.exit()
RunSim_forward.memory.InitMemory(MachineCodeParser.PC_INST, MachineCodeParser.DATA)
RunSim_forward.RunSim(reg_print=print_reg_file, buffprint=print_buff_file)

####################################################file dumping############################################################
#fileReg=open("RegisterDump.mc",'w')
#fileMem=open("MemoryDump.mc",'w')

# this fxn extends 0x2 to 0x00000002
def padhexa(s):
    return '0x' + s[2:].zfill(8)

#def print_reg(arr):  # input is numpy array
with open(f"RegisterDump_forward.mc", "w") as fileReg:
    for i in range(32): # for all 32 registers
        fileReg.write(f"x{i} ")  # print address of register for eg. x5
        if (RunSim_forward.registers.reg[i] >= 0):
            fileReg.write(padhexa(hex(RunSim_forward.registers.reg[i])).upper().replace('X', 'x'))
        else:
            reg = RunSim_forward.registers.reg[i] & 0xffffffff  # signed
            fileReg.write(hex(reg).upper().replace('X', 'x'))
        fileReg.write("\n")

#dumping memory
with open(f"MemoryDump_forward.mc", "w") as fileMem:  # input is dictionary with key as address and value as data
    lst = []  # stores keys present in dictionary
    temp_lst = []  # stores base address
    for key in RunSim_forward.memory.data_module.memory:
        lst.append(key)
    lst.sort()
    for x in lst:
        temp = x - (x % 4)  # storing base address in temp
        if temp not in temp_lst:  # if base address not present in temp_list , then append it
            temp_lst.append(temp)
    temp_lst.sort()
    for i in temp_lst:
        fileMem.write(f"{(padhexa(hex(i)).upper().replace('X', 'x'))} ")  # printing base address
        if i in lst:
            fileMem.write(f"{(padhexa(hex(RunSim_forward.memory.data_module.memory[i])).upper())[8:]} " )  # if key in dictionary, print its data
        else:
            fileMem.write("00 ")  # if key not in dictionary, print 00
        if (i + 1) in lst:
            fileMem.write(f"{(padhexa(hex(RunSim_forward.memory.data_module.memory[i + 1])).upper())[8:]} ")
        else:
            fileMem.write("00 ")
        if (i + 2) in lst:
            fileMem.write(f"{(padhexa(hex(RunSim_forward.memory.data_module.memory[i + 2])).upper())[8:]} ")
        else:
            fileMem.write("00 ")
        if (i + 3) in lst:
            fileMem.write(f"{(padhexa(hex(RunSim_forward.memory.data_module.memory[i + 3])).upper())[8:]} ")
        else:
            fileMem.write("00  ")
        fileMem.write("\n")  # new line
    lst = []  # stores keys present in dictionary
    temp_lst = []
    for key in RunSim_forward.memory.text_module.memory:
        lst.append(key)
    lst.sort()
    for x in lst:
        temp = x - (x % 4)  # storing base address in temp
        if temp not in temp_lst:  # if base address not present in temp_list , then append it
            temp_lst.append(temp)
    temp_lst.sort()
    for i in temp_lst:
        fileMem.write(f"{(padhexa(hex(i)).upper().replace('X', 'x'))} ")  # printing base address
        if i in lst:
            fileMem.write(f"{(padhexa(hex(RunSim_forward.memory.text_module.memory[i])).upper())[8:]} " )  # if key in dictionary, print its data
        else:
            fileMem.write("00 ")  # if key not in dictionary, print 00
        if (i + 1) in lst:
            fileMem.write(f"{(padhexa(hex(RunSim_forward.memory.text_module.memory[i + 1])).upper())[8:]} ")
        else:
            fileMem.write("00 ")
        if (i + 2) in lst:
            fileMem.write(f"{(padhexa(hex(RunSim_forward.memory.text_module.memory[i + 2])).upper())[8:]} ")
        else:
            fileMem.write("00 ")
        if (i + 3) in lst:
            fileMem.write(f"{(padhexa(hex(RunSim_forward.memory.text_module.memory[i + 3])).upper())[8:]} ")
        else:
            fileMem.write("00  ")
        fileMem.write("\n")  # new line
print("\033[1;92mRegister and memory outputs written in RegisterDump.mc and MemoryDump.mc respectively\033[0m")
