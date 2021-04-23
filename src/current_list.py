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

    def check_dependence(self, opcode,funct3,rs1,rs2,rd):
        #add data dependence check via registers
        i2=self.current_list[-1]   # this will contain the attributes of the function which was just before the current instruction
        i1=self.current_list[0]   # this will contain the attributes of the function which was
        dependency_i1=-1
        dependency_i2=-1

        if i2[0]==3:                # i2 is load and i3 is R type
            if opcode==51:
                if rs1 == i2[4] or rs2 == i2[4]:    # if rs1 or rs2 == to the register where value is being loaded
                    dependency_i2=2                    # In case we have a r type instruction just after load.
        if i2[0]==3:            # i2 is load and i3 is I type
            if opcode==19:
                if rs1==i2[4]:
                    dependency_i2=2

        if i2[0] == 3:  # if i2 is load and i3 is store type
            if opcode == 35:
                if i2[4] == rs2:   # if the rs2 or source of data is same as rd in load
                    dependency_i2=10



        if i1[0]==3:                # i1 is load and i3 is R type
            if opcode==51:
                if rs1 == i1[4] or rs2 == i1[4]:    # if rs1 or rs2 == to the register where value is being loaded
                    dependency_i1=2                    # In case we have a r type instruction just after load.

        if i1[0]==3:            # i1 is load and i3 is I type
            if opcode==19:
                if rs1==i1[4]:
                    dependency_i1=2

        if i1[0] == 3:  # if i1 is load and i3 is store type
            if opcode == 35:
                if i1[4] == rs2:    # if the rs2 or source of data is same as rd in load
                    dependency_i1=10

        #case16
        if i2[0] == 3:  # if i1 is load and i3 is store type
            if opcode == 35:
                if i2[4] == rs1:    # if the rs1 is same as rd in load
                    dependency_i1=16


        if i1[0] == 3:  # if i1 is load and i3 is store type
            if opcode == 35:
                if i1[4] == rs1:    # if the rs1 is same as rd in load
                    dependency_i1=16

        #odd Cases
        #Case1
        if i2[0]==51 or i2[0]==19 or i2[0]==23 or i2[0]==55:
            if opcode==51:
                if rs1==i2[4] or rs2==i2[4]:
                    dependency_i2=1
        if i1[0]==51 or i1[0]==19 or i2[0]==23 or i2[0]==55:
            if opcode==51:
                if rs1==i1[4] or rs2==i1[4]:
                    dependency_i1=1
        
        if i2[0]==51 or i2[0]==19 or i2[0]==23 or i2[0]==55:
            if opcode==19:
                if rs1==i2[4]:
                    dependency_i2=1
        if i1[0]==51 or i1[0]==19 or i2[0]==23 or i2[0]==55:
            if opcode==19:
                if rs1==i1[4]:
                    dependency_i1=1

        #Case 3
        if i2[0]==51 or i2[0]==19 or i2[0]==23 or i2[0]==55:
            if opcode==3:
                if rs1==i2[4]:
                    dependency_i2=3
        if i1[0]==51 or i1[0]==19 or i1[0]==23 or i1[0]==55:
            if opcode==3:
                if rs1==i1[4]:
                    dependency_i1=3

        #Case5
        if i2[0]==51 or i2[0]==19 or i2[0]==23 or i2[0]==55:
            if opcode==35:
                if rs1==i2[4] or rs2==i2[4]:
                    dependency_i2=5
        if i1[0]==51 or i1[0]==19 or i1[0]==23 or i1[0]==55:
            if opcode==35:
                if rs1==i1[4] or rs2==i1[4]:
                    dependency_i1=5

        #Case7
        if i2[0]==51 or i2[0]==19:
            if opcode==99:
                if rs1==i2[4] or rs2==i2[4]:
                    dependency_i2=7
        if i1[0]==51 or i1[0]==19:
            if opcode==99:
                if rs1==i1[4] or rs2==i1[4]:
                    dependency_i1=7

        #Case9
        if i2[0]==3:
            if opcode==99:
                if rs1==i2[4] or rs2==i2[4]:
                    dependency_i2=9
        if i1[0]==3:
            if opcode==99:
                if rs1==i1[4] or rs2==i1[4]:
                    dependency_i1=9

        #Case11

        #Case13:None
        #Case15:None

        return [dependency_i1,dependency_i2]


    def print_table(self):
        print(self.current_list[0])
        print(self.current_list[1])


#current=Current()
#current.add_inst(1, 2, 3, 4, 5)
#current.print_table()
#current.add_null()
#current.print_table()
