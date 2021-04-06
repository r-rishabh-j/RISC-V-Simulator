#!/usr/bin/python3
# ALU !
MAX_SIGNED_NUM = 0x7fffffff
MIN_SIGNED_NUM = -0x80000000
MAX_UNSIGNED_NUM = 0xffffffff
MIN_UNSIGNED_NUM = 0x00000000
MSmask32=0x80000000
bit_0_to_31_mask=0x7fffffff


class ArithmeticLogicUnit:
    def __init__(self):
        self.output32 = 0
        self.outputBool = False  # for branch instructions
        self.input1 = 0 # rs1
        self.input2 = 0 # rs2 or imm

    def ALUexecute(self, ALUop, ALUcontrol, inp1, inp2):
        if(ALUop==0): # ALU in NoOp condition
            print("hi")
            self.output32=0
            self.outputBool=False
            return 0
        self.input1=inp1
        self.input2=inp2
        if ALUcontrol==0:
            self.add()
        elif ALUcontrol==1:
            self.bitwiseAND()
        elif ALUcontrol==2:
            self.bitwiseOR()
        elif ALUcontrol==3:
            self.leftShift()
        elif ALUcontrol==4:
            self.rightShiftlogical()
        elif ALUcontrol==5:
            self.rightShiftarithmetic()
        elif ALUcontrol==6:
            # set if less than
            self.setIfLessThan()
        elif ALUcontrol==7:
            self.subtract()
        elif ALUcontrol==8:
            self.bitwiseXOR()
        elif ALUcontrol==9:
            self.multiply()
        elif ALUcontrol==10:
            self.division()
        elif ALUcontrol==11:
            self.remainder()
        elif ALUcontrol==12:
            self.AUIPC_LUI()
        elif ALUcontrol==13:
            self.areEqual()
        elif ALUcontrol==14:
            self.areNotEqual()
        elif ALUcontrol==15:
            self.GreaterThanEqualTo()
        elif ALUcontrol==16:
            self.LessThan()
        
    def add(self): # add, addi, lb, lw, lh, jalr, sb, sw, sh
        add=self.input1+self.input2
        add=(-(add&MSmask32)+(add&bit_0_to_31_mask)) # truncated and signed extended
        self.output32=add
        self.outputBool=True
        print(f"ALU- added {hex(self.input1)} and {self.input2}")
        return add

    def subtract(self): # sub
        sub=self.input1-self.input2
        sub=(-(sub&MSmask32)+(sub&bit_0_to_31_mask)) # truncated and signed extended
        self.output32=sub
        self.outputBool=True
        print(f"ALU- Subtracted {hex(self.input2)} from {self.input1}")
        return sub
    
    def AUIPC_LUI(self): # input1=PC, input2=imm20
        op1=self.input2&0xfffff
        op1<<=12
        out=self.input1+op1
        out=(-(out&MSmask32)+(out&bit_0_to_31_mask))
        self.output32=out
        self.outputBool=True
        return out

    # def LUI(self): # input1=rs1, input2=imm20
    #     op1=self.input2&0xfffff
    #     op1<<=12
    #     out=self.input1+op1
    #     out=(-(out&MSmask32)+(out&bit_0_to_31_mask))
    #     self.output32=out
    #     self.outputBool=True
    #     return out
    def setIfLessThan(self):
        self.outputBool=True if self.input1<self.input2 else False
        self.output32=self.outputBool
        return self.outputBool
        
    def multiply(self): # mul
        mult=self.input1*self.input2
        mult=(-(mult&MSmask32)+(mult&bit_0_to_31_mask)) # truncated and signed extended
        self.output32=mult
        self.outputBool=True
        print(f"ALU- multiplied {hex(self.input1)} and {self.input2}")
        return mult

    def division(self): # div
        if self.input2 == 0:
            raise Exception("Divide by 0 error")
        div=self.input1//self.input2 # floor division
        div=(-(div&MSmask32)+(div&bit_0_to_31_mask)) # truncated and signed extended
        self.output32=div
        self.outputBool=True
        print(f"ALU- Divided {hex(self.input1)} by {self.input2}")
        return div

    def remainder(self): # rem
        if self.input2 == 0:
            raise Exception("Divide by 0 error")
        mod=self.input1%self.input2 # floor division
        mod=(-(mod&MSmask32)+(mod&bit_0_to_31_mask)) # truncated and signed extended
        self.output32=mod
        self.outputBool=True
        print(f"ALU- Modulo of {hex(self.input1)} by {self.input2}")
        return mod

    def rightShiftlogical(self): # srl
        temp=self.input1&0xffffffff
        temp = (temp >> self.input2)
        temp=(-(temp&MSmask32)+(temp&bit_0_to_31_mask)) # truncated and signed extended
        self.output32=temp
        self.outputBool=True
        print(f"ALU- Logical right shift {self.input1} by {self.input2}")
        return temp

    def rightShiftarithmetic(self): # sra
        temp = (self.input1 >> self.input2)
        temp=(-(temp&MSmask32)+(temp&bit_0_to_31_mask)) # truncated and signed extended
        self.output32=temp
        self.outputBool=True
        print(f"ALU- Arithmetic right shift {self.input1} by {self.input2}")
        return temp

    def leftShift(self): #sll
        temp = (self.input1 << self.input2) & 0xffffffff
        temp=(-(temp&MSmask32)+(temp&bit_0_to_31_mask)) # truncated and signed extended
        self.output32=temp
        self.outputBool=True
        print(f"ALU- Leftshift {self.input1} by {self.input2}")
        return temp

    def bitwiseAND(self): # and, andi
        temp = (self.input1 & self.input2)
        temp=(-(temp&MSmask32)+(temp&bit_0_to_31_mask))
        self.output32=temp
        self.outputBool=True
        print(f"ALU- Bitwise AND {self.input1}, {self.input2}l")
        return temp

    def bitwiseXOR(self): #  xor
        temp = (self.input1 ^ self.input2)
        temp=(-(temp&MSmask32)+(temp&bit_0_to_31_mask))
        self.output32 = temp
        self.outputBool=True
        print(f"ALU- Bitwise XOR {self.input1}, {self.input2}l")
        return temp

    def bitwiseOR(self): # or, ori
        temp = (self.input1 | self.input2)
        temp=(-(temp&MSmask32)+(temp&bit_0_to_31_mask))
        self.output32 = temp
        self.outputBool=True
        print(f"ALU- Bitwise OR {self.input1}, {self.input2}l")
        return temp
    
    def areEqual(self): # beq
        if(self.input1==self.input2):
            self.outputBool=True
            self.output32=1
            return True
        else:
            self.outputBool=False
            self.output32=0
            return False

    def areNotEqual(self): # bne
        if(self.input1!=self.input2):
            self.outputBool=True
            self.output32=1
            return True
        else:
            self.outputBool=False
            self.output32=0
            return False
    
    def GreaterThanEqualTo(self): # rs1>=rs1, bge
        if(self.input1>=self.input2):
            self.outputBool=True
            self.output32=1
            return True
        else:
            self.outputBool=False
            self.output32=0
            return False

    def LessThan(self): # rs1<rs1, blt
        if(self.input1<self.input2):
            self.outputBool=True
            self.output32=1
            return True
        else:
            self.outputBool=False
            self.output32=0
            return False


# comparision operation TBD
