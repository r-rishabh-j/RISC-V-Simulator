#!/usr/bin/python3
# this file contains code for the simulator. Contains the ALU
from Registers import Registers as reg # contains 32 GP registers and PC,IR
from Memory import ProcessorMemoryInterface# processor memory interface
from ControlCircuit import ControlModule # generates control signals
from IAG import InstructionAddressGenerator
import ALU

MAX_SIGNED_NUM=0x7fffffff
MIN_SIGNED_NUM=-0x80000000
MAX_UNSIGNED_NUM=0xffffffff
MIN_UNSIGNED_NUM=0x00000000
# IR=0 # instruction register, holds the instruction to be executed
# PC=0 # program counter, holds pointer to memory location containing instruction
#
# reg=np.zeros(32) # 32 general purpose registers
# reg[2]=0x7ffffff0 # stack pointer sp
# reg[3]=0x10000000 # global pointer gp
# reg[4]=0x00000000 # thread pointer tp
# reg[5]=0x00000000 # frame pointer fp
registers=reg() # register object
memory=ProcessorMemoryInterface()
control_module=ControlModule()

def fetch():

def decode():
    control_module.decode(registers.ReadIR(True))
def execute(): # ALU

def mem_access():

def reg_writeback():


def RunSim():
    #loop
    fetch()
    decode()
    execute()
    mem_access()
    reg_writeback()
