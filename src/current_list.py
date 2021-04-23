#in transit instructions
from collections import deque

class Current:
    def __init__(self):
        self.current_list = deque([[-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1]])

    def add_inst(self, opcode, funct3, rs1, rs2, rd):
        self.current_list.popleft()
        inst_temp = [opcode, funct3, rs1, rs2, rd]
        self.current_list.append(inst_temp)

    def add_null(self):
        self.current_list.popleft()
        self.current_list.append([-1, -1, -1, -1, -1])

    def check_dependence(self, stage):
        #add data dependence check via registers



    def print_table(self):
        print(self.current_list[0])
        print(self.current_list[1])


#current=Current()
#current.add_inst(1, 2, 3, 4, 5)
#current.print_table()
#current.add_null()
#current.print_table()
