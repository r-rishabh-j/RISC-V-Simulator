import numpy as np

class registers:
    def __init__(self):
        self.IR=0 # instruction register, holds the instruction to be executed
        self.PC=0 # program counter, holds pointer to memory location containing instruction
        self.reg=np.zeros(32) # 32 general purpose registers
        self.reg[2]=0x7ffffff0 # stack pointer sp
        self.reg[3]=0x10000000 # global pointer gp
        self.reg[4]=0x00000000 # thread pointer tp
        self.reg[5]=0x00000000 # frame pointer fp