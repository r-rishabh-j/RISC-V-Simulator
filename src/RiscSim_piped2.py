#!/usr/bin/python3
# this file contains code for the simulator. Contains the ALU
from Registers import Registers as reg # contains 32 GP registers and IR
from Memory import ProcessorMemoryInterface# processor memory interface
from ControlCircuit import ControlModule # generates control signals
from IAG import InstructionAddressGenerator
from ALU import ArithmeticLogicUnit
from Buffers import Buffers
from Hazard import HazardUnit

MAX_SIGNED_NUM=0x7fffffff
MIN_SIGNED_NUM=-0x80000000
MAX_UNSIGNED_NUM=0xffffffff
MIN_UNSIGNED_NUM=0x00000000
registers=reg() # register object
memory=ProcessorMemoryInterface()
control_module=ControlModule()
ALUmodule=ArithmeticLogicUnit()
IAGmodule=InstructionAddressGenerator()
buffer=Buffers()
hazard_unit=HazardUnit()

# Muxes
MuxAout=0 # input 1 of ALU
MuxBout=0 # input 2 of ALU
MuxYout=0 # output of MuxY
def MuxB(MuxB_select):
    global MuxBout
    if MuxB_select==0:
        MuxBout=registers.ReadGpRegisters(control_module.rs2)
    elif MuxB_select==1:
        MuxBout=control_module.imm
    return MuxBout
def MuxA(MuxA_select):
    global MuxAout
    if MuxA_select==0:
        MuxAout=registers.ReadGpRegisters(control_module.rs1)
    elif MuxA_select==1:
        MuxAout=IAGmodule.PC
    return MuxAout
def MuxY(MuxY_select):
    global MuxYout
    if MuxY_select==0:
        MuxYout=buffer.getRZ()
    elif MuxY_select==1:
        MuxYout=memory.MDR
    elif MuxY_select==2:
        MuxYout=IAGmodule.PC_temp
    return MuxYout

###########Stage functions###############
def fetch(stage):
    # to do here
    # first, check the operation queue. If empty, then operate. Else, don't operate and pop.
    # fetch the instruction using the value in PC
    # compare it to BTB to check if that is a branch/jump. If it is, update PC to the target.

def decode(stage):
    # check the operation queue. If empty, then operate. Else, don't operate and pop.
    # decode the instruction first in the IR
    # check for hazards using the hazard table.
    # follow steps given in documentation to resolve the hazard by stalling/data forwarding.
    # if all good, push the decoded the signals into the queues.

def execute(stage): # ALU
    

def mem_access(stage):
   
def reg_writeback(stage):
    

def RunSim():
    

