# module to parse instructions in machine code and store them in PC_INST
import sys

PC_INST={} # dictionary with key as PC, value as instruction
DATA={} # dictionary with key as PC, value as instruction

# function to parse the instructions
# comments start with #
# comment feature is just for ease to paste code from venus
def parser(FileName):
    instructions=open(FileName,'r') # file containing the instructions
    # format-
    # PC INST -> in hex format
    line_number=0
    is_instruction=False
    for line in instructions:
        line_number=line_number+1
        line=line.strip() # removing unnecessary whitespaces \t, \n etc
        if(line=='~data'):
            is_instruction=0
            continue
        if(line=='~text'):
            is_instruction=1
            continue
        if line=='' or line[0]=='#': # ignores empty lines and commented lines.
            continue
        line=line.split('#')[0] # splitting the string into PC and INST word and ignoring comments
        line=line.strip().split()
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
                print(f"Line {line_number}: Invalid address")
                sys.exit()
        try:
            line[1]=int(line[1]) # interpreted as base 10
        except:
            try:
                line[1]=int(line[1], 16) # interpreted as base 16
            except:
                print(f"Line {line_number}: Invalid instruction format")
                sys.exit()
        if(line[0]>0x7fffffff):
            print(f"Line {line_number}: Address out of range")
            sys.exit()
        
        if is_instruction==1:
            PC_INST[line[0]]=line[1]
        else:
            DATA[line[0]]=line[1]

    instructions.close()
        #print(line)
    