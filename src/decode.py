#decode machine code
import math

#addi 19 0
#andi 19 7
#ori 19 6
#lb 3 0
#lh 3 1
#lw 3 2
#jalr 103 0
I = [19, 3, 103] #opcodes for I

#sb 35 0
#sh 35 1
#sw 35 2
S = [35] #opcode for S

#auipc 23
#lui 55
U = [23, 55]  #opcodes for U

#add 51 0 0
#and 51 7 0
#or 51 6 0
#sll 51 1 0
#slt 51 2 0
#sra 51 5 32
#srl 51 5 0
#sub 51 0 32
#xor 51 4 0
#mul 51 0 1
#div 51 4 1
#rem 51 6 1
R = [51]  #opcode for R
SB = [99]  #opcode for SB
UJ = [111] #opcode for UJ

def decodeI(temp):
    inst_list = []
    temp = temp >> 7
    inst_list.append((temp & 0x1f));    #rd
    temp = temp >> 5
    inst_list.append((temp & 0x3));     #funct3
    temp = temp >> 3
    inst_list.append((temp & 0x1f));    #rs1
    temp = temp >> 5
    inst_list.append((-(temp & 0x800) | (temp & 0x7ff)))    #imm(signed)
    #print(inst_list)
    return inst_list
    
def decodeS(temp):
    inst_list = []
    temp = temp >> 7
    temp1 = temp & 0x1f     #building the register in temp1
    temp = temp >> 5
    inst_list.append((temp & 0x3))  #funct3
    temp = temp >> 3
    inst_list.append((temp & 0x1f)) #rs1
    temp = temp >> 5
    inst_list.append((temp & 0x1f)) #rs2
    temp = temp >> 5
    temp = temp << 5
    temp1 = temp1+temp
    inst_list.append((-(temp1 & 0x800) | (temp1 & 0x7ff)))    #imm(signed)
    return inst_list   

def decodeU(temp):
    inst_list = []
    temp = temp >> 7
    inst_list.append((temp & 0x1f))     #rd
    temp = temp >> 5
    inst_list.append((-(temp & 0x80000) | (temp & 0x7ffff)))    #upper-imm(signed)
    return inst_list
    
def decodeR(temp):
    inst_list = []
    temp = temp >> 7
    inst_list.append((temp & 0x1f));    #rd
    temp = temp >> 5
    inst_list.append((temp & 0x3));     #funct3
    temp = temp >> 3
    inst_list.append((temp & 0x1f));    #rs1
    temp = temp >> 5
    inst_list.append((temp & 0x1f));    #rs2
    temp = temp >> 5
    inst_list.append((temp & 0x7f));    #funct7
    return inst_list
    
def decodeSB(n):
    inst_list = []
    func3=n & 0x000007000  
    func3=func3>>12
    inst_list.append(func3) #funct3
    r1=n & 0x000F8000
    r1=r1>>15
    inst_list.append(r1)  #rs1
    r2=n & 0x01F00000
    r2=r2>>20
    inst_list.append(r2)   #rs2
    temp=n>>7
    temp11=temp & 0x01   #imm[11]
    temp11=temp11<<11
    temp1=n>>8
    temp1=temp1 & 0x0F  #imm[4:1]
    temp1=temp1<<1
    temp5=n>>25
    temp5=temp5 & 0x03F  #imm[10:5]
    temp5=temp5<<5
    temp12=n>>31
    temp12=temp12<<12   #imm[12]
    immf=temp12+temp11+temp5+temp1  #finding final imm
    im=(-(immf & 0x1000)| (immf& 0x0FFF))  #making it signed
    inst_list.append(im)
    return inst_list
    
def decodeUJ(n):
    inst_list = []
    rdd=n & 0x00000F80 
    rdd=rdd>>7
    inst_list.append(rdd)   #rd
    temp12=n>>12
    temp12=temp12 & 0x0FF
    temp12=temp12<<12  #imm[19:12]
    temp11=n>>20
    temp11=temp11 & 0x01
    temp11=temp11<<11  #imm[11]
    temp1=n>>21
    temp1=temp1 & 0x03FF
    temp1=temp1<<1   #imm[10:1]
    temp20=n>>31
    temp20=temp20<<20  #immp[20]
    immf=temp20+temp12+temp11+temp1  #final imm
    im=(-(immf & 0x100000)|(immf & 0x0FFFFF));  #making it signed
    inst_list.append(im)
    return inst_list
    
def decode(hex_string):
    #while True:
        #instruction = input().split(' ');
        #if instruction[1] == "0x00000000":
            #print("Done decoding all instructions!")
            #break
        #PC = int(instruction[0], 16)
        #temp = int(hex_string, 16)
        opcode = (temp & 0x7f)
        #print(opcode, temp)
        if opcode in I:
            inst_list = decodeI(temp)
            rd = inst_list[0]
            funct3 = inst_list[1]
            rs1 = inst_list[2]
            imm = inst_list[3]
            #print(PC, "I type", opcode, funct3, rs1, rd, imm)
        elif opcode in S:
            inst_list = decodeS(temp)
            funct3 = inst_list[0]
            rs1 = inst_list[1]
            rs2 = inst_list[2]
            imm = inst_list[3]
            #print(PC, "S type", opcode, funct3, rs1, rs2, imm)
        elif opcode in U:
            inst_list = decodeU(temp)
            rd = inst_list[0]
            imm = inst_list[1]
            #print(PC, "U type", opcode, rd, imm)
        elif opcode in R:
            inst_list = decodeR(temp)
            rd = inst_list[0]
            funct3 = inst_list[1]
            rs1 = inst_list[2]
            rs2 = inst_list[3]
            funct7 = inst_list[4]
            #print(PC, "R type", opcode, funct3, funct7, rs1, rs2, rd)
        elif opcode in SB:
            inst_list = decodeSB(temp)
            funct3 = inst_list[0]
            rs1 = inst_list[1]
            rs2 = inst_list[2]
            imm = inst_list[3]
            #print(PC, "SB type", opcode, funct3, rs1, rs2, imm)
        elif opcode in UJ:
            inst_list = decodeUJ(temp)
            rd = inst_list[0]
            imm = inst_list[1]
            #print(PC, "UJ type", opcode, rd, imm)
        else:
            raise Exception("Not an instruction")
