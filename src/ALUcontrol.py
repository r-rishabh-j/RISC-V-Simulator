def ALUcontrolgenerator(opcode, funct3, funct7):
    if opcode == 51:
        if funct3 == 0:
            if funct7 == 0:
                return 0
            elif funct7 == 32:
                return 7
            elif funct7 == 1:
                return 9
        elif funct3 == 7:
            if funct7 == 0:
                return 1
        elif funct3 == 6:
            if funct7 == 0:
                return 2
            elif funct7 == 1:
                return 11
        elif funct3 == 1:
            return 3
        elif funct3 == 5:
            if funct7 == 0:
                return 4
            elif funct7 == 32:
                return 5
        elif funct3 == 2:
            if funct7 == 0:
                return 6
        elif funct3 == 4:
            if funct7 == 0:
                return 8
            elif funct7 ==1:
                return 10
        else:
            raise Exception("Not a valid Instruction")
    elif opcode == 19:
        if funct3 == 0 and funct7 == 0:
            return 0
        elif funct3 == 7 and funct7 == 0:
            return 1
        elif funct3 == 6 and funct7 == 0:
            return 2
        else:
            raise Exception("Not a valid Instruction")
    elif opcode == 3:
        if funct3 in [0, 1, 2] and funct7 == 0:
            return 0
        else:
            raise Exception("Not a valid Instruction")
    elif opcode == 103:
        if funct3 == 0 and funct7 == 0:
            return 0
        else:
            raise Exception("Not a valid Instruction")
    elif opcode == 35:
        if funct3 in [0, 1, 2] and funct7 == 0:
            return 0
        else:
            raise Exception("Not a valid Instruction")
    elif opcode == 23:
        if funct3 == 0 and funct7 == 0:
            return 12
        else:
            raise Exception("Not a valid Instruction")
    elif opcode == 55:
        if funct3 == 0 and funct7 == 0:
            return 12
        else:
            raise Exception("Not a valid Instruction")
    elif opcode == 111:
        if funct3 == 0 and funct7 == 0:
            return 0
        else:
            raise Exception("Not a valid Instruction")
    elif opcode == 99:
        if funct3 == 0 and funct7 == 0:
            return 13
        elif funct3 == 1 and funct7 == 0:
            return 14
        elif funct3 == 5 and funct7 == 0:
            return 15
        elif funct3 == 4 and funct7 == 0:
            return 16
        else:
            raise Exception("Not a valid Instruction")
    else:
        raise Exception("Not a valid Instruction")