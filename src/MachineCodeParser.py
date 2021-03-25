# module to parse instructions in machine code and store them in PC_INST
import sys

PC_INST={} # dictionary with key as PC, value as instruction

# function to parse the instructions
def parser(FileName):
    instructions=open(FileName,'r') # file containing the instructions
    # format-
    # PC INST -> in hex format, other formats not supported as of now
    line_number=0
    for line in instructions:
        line_number=line_number+1
        line=line.strip() # removing unnecessary whitespaces \t, \n etc
        if line=='' or line[0]=='#': # ignores empty lines and commented lines. Comment in the same line with a command not supported!
            continue
        #print(f"\'{line}\'")
        line=line.split() # splitting the string into PC and INST word
        # PC_INST[line[0]]=line[1] # this was tried to store PC and instructions as strings in the dict. May be required in the future.
        #print(line)
        if len(line)!=2: # line should contain exactly 2 items.
            print(f"Line {line_number}: Invalid syntax")
            sys.exit()
        # parser will treat numbers entered without 0x as decimal, and with 0x as hexadecimal
        try:
            line[0]=int(line[0]) # interpreted as base 10
        except: # number entered is not decimal
            try:
                line[0]=int(line[0],16) # interpreted as base 16
            except: # str is neither decimal nor hex
                print(f"Line {line_number}: Invalid program counter (PC)")
                sys.exit()
        try:
            line[1]=int(line[1]) # interpreted as base 10
        except:
            try:
                line[1]=int(line[1], 16) # interpreted as base 16
            except:
                print(f"Line {line_number}: Invalid instruction format")
                sys.exit()
        PC_INST[line[0]]=line[1]
        #print(line)
    