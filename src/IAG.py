# this is the module which calculates the next PC value based on the input control signals.
import sys

class InstructionAddressGenerator:
    MAX_SIGNED_NUM = 0x7fffffff
    MIN_SIGNED_NUM = -0x80000000
    MAX_UNSIGNED_NUM = 0xffffffff
    MIN_UNSIGNED_NUM = 0x00000000
    MAX_PC = 0x7ffffffc

    def __init__(self):
        self.PC=0  #this is the PC register which starts from 0
        self.PC_temp=0 # temp pc which stores PC+4
        self.IAGimmediate=0 # branch offset , this is the immediate value


    def PcTempUpdate(self):     # this is the function for 1st step which will store the value of PC+4 in register temppc
        self.temppc=self.PC+4


    def Pcset(self,ra,MuxPCSelect):  # to chose the output of MuxPc , RA or PC itself , after this the offset would be added In func PcUpdate
        if MuxPCSelect==1:             # if this control signal is 1 then put the value of ra (which would be given by register in jalr instruction ) would be given to PC
            self.PC=ra


    def SetBranchOffset(self,boffset):      # this will take as input the immediate value which will be supplied after the decode step
        self.IAGimmediate=boffset

    def PcUpdate(self,MuxINCSelect):   # in this step we will get the mux select line from control based on the comparison operations performed by the ALU , which decides whether to jump or to not
        if MuxINCSelect==0:    # if mux select is 0 then add 4 to PC
            self.PC+=4
        elif MuxINCSelect==1:  # in case mux select is 1 then add immediate / offset to PC
            self.PC+=self.IAGimmediate
            if self.PC > self.MAX_PC:
                print("Address is not in range of data segment")
                sys.exit()
                
# at the end of this , if all functions are called sequentially we will have the required value of PC in the register PC
# here using this function at the end the value of temppc is also supplied to MuxY , which is the step before write back.(only used in case of JAL like instructions)