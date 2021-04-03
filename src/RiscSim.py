#!/usr/bin/python3
# this file contains code for the simulator. Contains the ALU
from registers import registers as reg # contains 32 GP registers and PC,IR
from memory import ByteAddressableMemory# processor memory interface
import ControlCircuit # generates control signals
import ALU

MAX_SIGNED_NUM=0x7fffffff
MIN_SIGNED_NUM=0x10000000
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
register=reg() # register object

def fetch():

def decode():

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
