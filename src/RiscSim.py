#!/usr/bin/python3
# this file contains code for the simulator. Contains the ALU
from Registers import Registers as reg # contains 32 GP registers and PC,IR
from Memory import ProcessorMemoryInterface# processor memory interface
from ControlCircuit import ControlModule # generates control signals
from IAG import InstructionAddressGenerator
from ALU import ArithmeticLogicUnit
import Mux

MAX_SIGNED_NUM=0x7fffffff
MIN_SIGNED_NUM=-0x80000000
MAX_UNSIGNED_NUM=0xffffffff
MIN_UNSIGNED_NUM=0x00000000
registers=reg() # register object
memory=ProcessorMemoryInterface()
control_module=ControlModule()
ALUmodule=ArithmeticLogicUnit()
IAGmodule=InstructionAddressGenerator()
#buffer registers
RZ=0
RM=0
RY=0
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
        MuxYout=RZ
    elif MuxY_select==1:
        MuxYout=memory.MDR
    elif MuxY_select==2:
        MuxYout=IAGmodule.PC_temp
    return MuxYout

###########Stage functions###############
def fetch():

def decode():
    control_module.decode(registers.ReadIR(True))
    #decode

    #loading the register values
    MuxAout=MuxA(control_module.MuxAselect)
    MuxBout=MuxB(control_module.MuxBselect)
def execute(): # ALU
    # ALUmodule.input1=MuxA(control_module.MuxAselect)
    # ALUmodule.input2=MuxB(control_module.MuxBselect)
    #ALUmodule.ALUexecute(control_module.ALUop, control_module.ALUcontrol, MuxA(control_module.MuxAselect), MuxB(control_module.MuxBselect))

def mem_access():

def reg_writeback():


def RunSim():
    #loop
    fetch()
    decode()
    execute()
    mem_access()
    reg_writeback()
