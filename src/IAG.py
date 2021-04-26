# this is the module which calculates the next PC value based on the input control signals.
import sys

class BTB_entry:
    def __init__(self):
        self.inst_address=0;  # this is the value of the instruction itself
        self.target_address=0; # this is the value of the target address
        self.take=0;# this is 1 if the target is to be taken or not

class InstructionAddressGenerator:
    MAX_SIGNED_NUM = 0x7fffffff
    MIN_SIGNED_NUM = -0x80000000
    MAX_UNSIGNED_NUM = 0xffffffff
    MIN_UNSIGNED_NUM = 0x00000000
    MAX_PC = 0x7ffffffc

    def __init__(self):
        self.PC=0  #this is the PC register which starts from 0
        self.PC_temp=0 # temp pc which stores PC+4
        self.PC_buffer=0
        self.IAGimmediate=0 # branch offset , this is the immediate value
        self.BTB=dict() # key as PC and entry is a variable of the class BTB_entry

    def ReadPC(self):
        PCval=self.PC
        return PCval

    def WritePC(self, WriteVal, writePC):
        if(writePC==True):
            self.PC=WriteVal

    def PCTempUpdate(self):     # this is the function for 1st step which will store the value of PC+4 in register temppc
        self.PC_temp=self.PC+4


    def PCset(self,RA,MuxPCSelect):  # to chose the output of MuxPc , RA or PC itself , after this the offset would be added In func PcUpdate
        if MuxPCSelect==0:             # if this control signal is 1 then put the value of ra (which would be given by register in jalr instruction ) would be given to PC
            self.PC_buffer=RA

    def SetBranchOffset(self,boffset):      # this will take as input the immediate value which will be supplied after the decode step
        self.IAGimmediate=boffset

    def PCUpdate(self,MuxINCSelect):   # in this step we will get the mux select line from control based on the comparison operations performed by the ALU , which decides whether to jump or to not
        if MuxINCSelect==0:    # if mux select is 0 then add 4 to PC
            self.PC_buffer+=4
        elif MuxINCSelect==1:  # in case mux select is 1 then add immediate / offset to PC
            self.PC_buffer+=self.IAGimmediate
            print(f"IAG!!!!!!!!!!!!!!!!!!!!!!!!!!!! {self.PC_buffer} {self.IAGimmediate}")
            if self.PC_buffer > self.MAX_PC:
                print("Address is not in range of data segment")
                sys.exit()
    # def PCUpdate(self,MuxINCSelect):   # in this step we will get the mux select line from control based on the comparison operations performed by the ALU , which decides whether to jump or to not
    #     if MuxINCSelect==0:    # if mux select is 0 then add 4 to PC
    #         self.PC+=4
    #     elif MuxINCSelect==1:  # in case mux select is 1 then add immediate / offset to PC
    #         self.PC+=self.IAGimmediate
    #         if self.PC > self.MAX_PC:
    #             print("Address is not in range of data segment")
    #             sys.exit()

    def BTB_check(self,Inst_PC_Value):  # to check wether a particular control instruction is present in the table or not.
        if Inst_PC_Value in self.BTB:   # if the instruction is already present in the BTB then 1 is returned else 0
            return 1
        else :
            return 0

    def BTB_insert(self,Inst_PC_Value,Inst_Target_Value,Take):   # the table would be indexed using PC_value and Take will be 1 if Inst_Target_Value would shoukd be taken or not
        temp_BTB_entry=BTB_entry()    # temporary object of BTB entry
        temp_BTB_entry.inst_address=Inst_PC_Value        # assigning the values of this temporary object to be the passed arguments
        temp_BTB_entry.target_address=Inst_Target_Value
        temp_BTB_entry.take=Take
        self.BTB[Inst_PC_Value]=temp_BTB_entry

# at the end of this , if all functions are called sequentially we will have the required value of PC in the register PC
# here using this function at the end the value of temppc is also supplied to MuxY , which is the step before write back.(only used in case of JAL like instructions)