#control signals generator
def ControlSignalGenerator(opcode, funct3):
    if opcode == 51:    #R-type
        ALUOp = 1       #ALU usage required
        MuxBSelect = 0  #no immediate
        MuxYSelect = 0  #choose output of ALU in RZ
        BytestoRead = 0
        BytestoWrite = 0
        RegWrite = 1    #update register
        MuxINCSelect = 0    #sequentially next PC
        MuxASelect = 0      #rs1
        branch = 0          #required to update control for branch inst
        MuxPCSelect = 1     #not ra
        #MuxMASelect = 1     #PC send to MAR in step1
        MemRead = False
        MemWrite = False
    elif opcode == 19:    #I-type (ori, andi, addi)
        ALUOp = 1
        MuxBSelect = 1     #imm value used in MuxB
        MuxYSelect = 0      #choose output of ALU in RZ
        BytestoRead = 0
        BytestoWrite = 0
        RegWrite = 1    #update register
        MuxINCSelect = 0    #sequentially next PC
        MuxASelect = 0      #rs1
        branch = 0          #required to update control for branch inst
        MuxPCSelect = 1     #not ra
        #MuxMASelect = 1     #PC send to MAR in step1
        MemRead = False
        MemWrite = False
    elif opcode == 3:   #I-type(load-instructions)
        ALUOp = 1       #ALU used to calculate effective address
        MuxBSelect = 1     #imm value used in MuxB
        MuxYSelect = 1  #MDR value selected
        if funct3 == 0:     #lb
            BytestoRead = 1
        if funct3 == 1:   #lh
            BytestoRead = 2
        if funct3 == 2:   #lw
            BytestoRead = 4
        BytestoWrite = 0
        RegWrite = 1    #update register
        MuxINCSelect = 0    #sequentially next PC
        MuxASelect = 0      #rs1
        branch = 0          #required to update control for branch inst
        MuxPCSelect = 1     #not ra
        #MuxMASelect = 1     #PC send to MAR in step1
        MemRead = True
        MemWrite = False
    elif opcode == 103:     #I-type(jalr)
        ALUOp = 0   #ALU not used, done in IAG
        MuxBSelect = 0  #don't-care
        MuxYSelect = 2  #ra given to MuxY
        BytestoRead = 0
        BytestoWrite = 0
        RegWrite = 1    #update register
        MuxINCSelect = 1
        MuxASelect = 0      #rs1
        branch = 0          #required to update control for branch inst
        MuxPCSelect = 0     #ra input to MuxPC
        #MuxMASelect = 1     #PC send to MAR in step1
        MemRead = False
        MemWrite = False
    elif opcode == 35:      #S-type
        ALUOp = 1   #ALU used to calculate effective address
        MuxBSelect = 1  #imm value used in MuxB
        MuxYSelect = 0  #don't-care
        BytestoRead = 0
        if funct3 == 0: #sb
            BytestoWrite = 1
        if funct3 == 1: #sh
            BytestoWrite = 2
        if funct3 == 2: #sw
            BytestoWrite = 4
        RegWrite = 0    #Register update not required
        MuxINCSelect = 0    #sequentially next PC
        MuxASelect = 0      #rs1
        branch = 0          #required to update control for branch inst
        MuxPCSelect = 1     #not ra
        #MuxMASelect = 1     #PC send to MAR in step1
        MemRead = False
        MemWrite = True
    elif opcode == 23 :  #U-type(auipc)
        ALUOp = 1
        MuxBSelect = 1
        MuxYSelect = 0  #choose output of ALU in RZ
        BytestoRead = 0
        BytestoWrite = 0
        RegWrite = 1
        MuxINCSelect = 0    #sequentially next PC
        MuxASelect = 1      #PC as input1 of ALU
        branch = 0          #required to update control for branch inst
        MuxPCSelect = 1     #not ra
        #MuxMASelect = 1     #PC send to MAR in step1
        MemRead = False
        MemWrite = False
    elif opcode == 55:  #U-type(lui)
        ALUOp = 1
        MuxBSelect = 1
        MuxYSelect = 0  #choose output of ALU in RZ
        BytestoRead = 0
        BytestoWrite = 0
        RegWrite = 1
        MuxINCSelect = 0    #sequentially next PC(4)
        MuxASelect = 0      #rs1
        branch = 0          #required to update control for branch inst
        MuxPCSelect = 1     #not ra
        #MuxMASelect = 1     #PC send to MAR in step1
        MemRead = False
        MemWrite = False
    elif opcode == 111: #UJ-type(jal)
        ALUOp = 0   #ALU not required, done in IAG
        MuxBSelect = 0  #don't-care
        MuxYSelect = 2  #ra given to MuxY
        BytestoRead = 0
        BytestoWrite = 0
        RegWrite = 1    #update register
        MuxINCSelect = 1
        MuxASelect = 0      #rs1
        branch = 0          #required to update control for branch inst
        MuxPCSelect = 1     #not ra
        #MuxMASelect = 1     #PC send to MAR in step1
        MemRead = False
        MemWrite = False
    elif opcode == 99:  #SB type
        ALUOp = 1
        MuxBSelect = 0  #rs2 is required, imm is used in IAG
        MuxYSelect = 2  #ra, but don't-care
        BytestoRead = 0
        BytestoWrite = 0
        RegWrite = 0    #do not update register
        MuxINCSelect = 0   #to be updated after ALU
        MuxASelect = 0      #rs1
        branch = 1          #required to update control for branch inst
        MuxPCSelect = 1     #not ra
        #MuxMASelect = 1     #PC send to MAR in step1
        MemRead = False
        MemWrite = False
        
