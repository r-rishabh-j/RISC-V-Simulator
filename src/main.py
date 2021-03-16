# !/usr/bin/python3
import MachineCodeParser # import parser for parsing machine code into PC and corresponding instructions.

MachineCodeParser.parser("instructions.mc") # supply input file name
print(MachineCodeParser.PC_INST)