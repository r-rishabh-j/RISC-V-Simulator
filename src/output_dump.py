#!/usr/bin/python3
import numpy as np

# this fxn extends 0x2 to 0x00000002
def padhexa(s):
    return '0x' + s[2:].zfill(8)

def print_reg(arr):
    for i in range(32):
        print("x",i," ",sep="",end="") # print address of register for eg. x5
        if(arr[i]>=0):
            print(padhexa(hex(arr[i])))    
        else:
            reg=arr[i] & 0xffffffff  # signed
            print(hex(reg))
            
#for checking
# arr = np.array([1, -2, 3])
# print_reg(arr)

# dumping memory
def print_mem(dic):
    lst=[] # stores keys present in dictionary
    temp_lst=[] # stores base address
    for key in dic:
        lst.append(key)
    lst.sort()
    for x in lst:
        temp = x - (x % 4)  # storing base address in temp
        if temp not in temp_lst: # if base address not present in temp_list , then append it
            temp_lst.append(temp)
    temp_lst.sort()
    for i in temp_lst:
        print(padhexa(hex(i)),end=" ")  # printing base address
        if i in lst:
            print(padhexa(hex(dic[i]))[8:],end=" ") # if data in dictionary
        else:
            print("00",end=" ") # if data not in dictionary
        if (i+1) in lst:
            print(padhexa(hex(dic[i+1]))[8:],end=" ")
        else:
            print("00",end=" ")
        if (i+2) in lst:
            print(padhexa(hex(dic[i+2]))[8:],end=" ")
        else:
            print("00",end=" ")
        if (i+3) in lst:
            print(padhexa(hex(dic[i+3]))[8:],end=" ")
        else:
            print("00",end=" ")
        print() # new line

# for checking
# dic = {19:3,4:11,6:7,241:241}
# print_mem(dic)