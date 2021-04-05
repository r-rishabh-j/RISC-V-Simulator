#!/usr/bin/python3
# ALU !
MAX_SIGNED_NUM = 0x7fffffff
MIN_SIGNED_NUM = -0x80000000
MAX_UNSIGNED_NUM = 0xffffffff
MIN_UNSIGNED_NUM = 0x00000000


class ArithmeticLogicUnit:
    def __init__(self):
        self.output32 = 0
        self.outputBool = False  # for branch instructions
        self.input1 = 0
        self.input2 = 0

    def ALUexecute(self, control, inp1, inp2):


    def add(self):
        temp = (self.input1 + self.input2) & 0xffffffff
        if temp != self.input1 + self.input2:
            raise Exception("Overflow error")
        else:
            self.output32 = temp
        print("Addition successful")

    def subtract(self):
        temp = (self.input1 - self.input2) & 0xffffffff
        if temp != self.input1 - self.input2:
            raise Exception("Overflow error")
        else:
            self.output32 = temp
        if temp == 0:
            self.outputBool = True
        print("Subtraction successful")

    def multiply(self):
        temp = (self.input1 * self.input2) & 0xffffffff
        if temp != self.input1 * self.input2:
            raise Exception("Overflow error")
        else:
            self.output32 = temp
        print("Multiplication successful")

    def division(self):
        if self.input2 == 0:
            raise Exception("Second argument cannot be 0")
        temp = (self.input1 / self.input2) & 0xffffffff
        if temp != self.input1 / self.input2:
            raise Exception("Overflow error")
        else:
            self.output32 = temp
        print("Division successful")

    def remainder(self):
        if self.input2 == 0:
            raise Exception("Second argument cannot be 0")
        temp = (self.input1 % self.input2) & 0xffffffff
        if temp != self.input1 % self.input2:
            raise Exception("Overflow error")
        else:
            self.output32 = temp
        print("Modulus successful")

    def rightShift(self):

    def rightShiftlogical(self):
        temp = (self.input1 >> self.input2) & 0xffffffff
        if temp != self.input1 >> self.input2:
            raise Exception("Overflow error")
        else:
            self.output32 = temp
        print("Logical right shift successful successful")

    def rightShiftarithmetic(self):
        if self.input1 & 2 ** (32 - 1) != 0:  # MSB is 1, i.e. x is negative
            filler = int('1' * self.input2 + '0' * (32 - self.input2), 2)
            self.output32 = (self.input1 >> self.input2) | filler  # fill in 0's with 1's
        else:
            self.output32 = self.input1 >> self.input2
        print("Arithmetic right shift successful")

    def leftShift(self):
        temp = (self.input1 << self.input2) & 0xffffffff
        if temp != self.input1 >> self.input2:
            raise Exception("Overflow error")
        else:
            self.output32 = temp
        print("Left shift successful successful")

    def bitwiseAND(self):
        temp = (self.input1 & self.input2)
        self.output32 = temp
        print("And successful")

    def bitwiseXOR(self):
        temp = (self.input1 ^ self.input2)
        self.output32 = temp
        print("XOR successful")

    def bitwiseOR(self):
        temp = (self.input1 | self.input2)
        self.output32 = temp
        print("OR successful")

# comparision operation TBD
