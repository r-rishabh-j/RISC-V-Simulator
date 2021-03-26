# !/usr/bin/python3
import MachineCodeParser # import parser for parsing machine code into PC and corresponding instructions.

MachineCodeParser.parser("instructions.mc") # supply input file name
for key in MachineCodeParser.PC_INST:
    print(hex(key),hex(MachineCodeParser.PC_INST[key]))