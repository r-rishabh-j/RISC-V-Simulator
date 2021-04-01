#!/usr/bin/python3
# this file contains code for the simulator. Contains the ALU
import numpy as np
import memory # processor memory interface
import ControlCircuit # generates control signals

IR=0 # instruction register, holds the instruction to be executed 
PC=0 # program counter, holds pointer to memory location containing instruction

reg=np.zeros(32) # 32 general purpose registers
reg[2]=0x7ffffff0 # stack pointer sp
reg[3]=0x10000000 # global pointer gp
reg[4]=0x00000000 # thread pointer tp
reg[5]=0x00000000 # frame pointer fp

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
    mem_writeback()

# run sim
RunSim()  