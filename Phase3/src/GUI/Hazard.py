# 3 types of stalls- decode stall, fetch stall and execute stall
# RAW data hazards-
# Case1- between D and

    #in transit instructions
from collections import deque

# class Current:
class HazardUnit:
    def __init__(self):
        self.current_list = deque([[-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1]])
        self.inst_table = deque()

    def add_inst(self, opcode, funct3, rs1, rs2, rd):
        self.current_list.popleft()
        inst_temp = [opcode, funct3, rs1, rs2, rd]
        self.current_list.append(inst_temp)

    def add_null(self):
        self.current_list.popleft()
        self.current_list.append([-1, -1, -1, -1, -1])


    def data_forwarding(self,i1,i2):     # to determine the type of forwarding and stalling
        i2_forwarding=-1
        i1_forwarding=-1
        
        #first dealing with all cases of i2 and i3 dependence if these does not exist, then only going to i1
        # Case 1 , dependancy with i2
        if i2== 103:
            i2_forwarding=33
            return [i1_forwarding,i2_forwarding]

        # i2 to rs1, then the possible cases of rs2
        if i2 == 101:
            i2_forwarding=31

            # Case 1 with i1 to rs2
            if i1 == 102:
                i1_forwarding=22
            # Case 2 with i1 to rs2
            if i1 == 202:
                i1_forwarding=12

            return [i1_forwarding,i2_forwarding]

        # i2 to rs2 , then the possible cases of rs1
        if i2 == 102:
            i2_forwarding = 32

            # Case 1 with i1 to rs1
            if i1 == 101:
                i1_forwarding = 21
            # Case 2 with i1 to rs1
            if i1 == 201:
                i1_forwarding = 11

            return [i1_forwarding, i2_forwarding]

        # in case only rs1 is present and no rs2
        if i2==1:
            i2_forwarding=31
            return [i1_forwarding,i2_forwarding]

        # case 2 , dependency with i2

        # from i2 to both rs1 and rs2
        if i2==203:
            i2_forwarding=23
            return [i1_forwarding,i2_forwarding]

        # from i2 to rs1
        if i2==201:
            i2_forwarding=21
            # Case 1 with i1 to rs2
            if i1 == 102:
                i1_forwarding = 22
            # Case 2 with i1 to rs2
            if i1 == 202:
                i1_forwarding = 12

            return [i1_forwarding, i2_forwarding]

        # i2 to rs2
        if i2==202:
            i2_forwarding=22

            # Case 1 with i1 to rs1
            if i1 == 101:
                i1_forwarding = 21
            # Case 2 with i1 to rs1
            if i1 == 201:
                i1_forwarding = 11

            return [i1_forwarding, i2_forwarding]

        # in case only rs1 is present ,in I type instrux:-
        # forwarding to i2 rd to rs1 and no forwards from i1
        if i2==2:
            i2_forwarding=21

            return [i1_forwarding, i2_forwarding]
        #case 3, dependency with i2:-

        # here only forwarding to rs1 is possible : -
        if i2==3:
            i2_forwarding=31
            return [i1_forwarding,i2_forwarding]


        # Case 9 ,checking dependancy with i2:-

        if i2==9:
            i2_forwarding=505
            i1_forwarding=-1
            return [i1_forwarding,i2_forwarding]

        # case 13 , checking dependancy with i2:-
        if i2==13:
            i2_forwarding = 505
            i1_forwarding = -1
            return [i1_forwarding, i2_forwarding]

        # case 17 , checking dependance with i2:-
        # if i2 is going to rs1:-
        if i2==1701:

            # only dependant on i2 and not i1 (or i2 is given prefrence)
            if i1==-1 or i1==1701 or i1==1801:
                i2_forwarding=31

            # case 17
            # i1 to rs2 and i1 is R type
            if i1==1702:
                i1_forwarding=404
                i2_forwarding=-1

            #case 18
            # i1 to rs2 and i1 is lw/jalr/jal type:-
            if i1==1802:
                i1_forwarding = 404
                i2_forwarding = -1

            return [i1_forwarding,i2_forwarding]

        # if i2 is going to rs2:-
        if i2 == 1702:

            # only dependant on i2 and not i1 (or i2 is given prefrence)
            if i1==-1 or i1==1702 or i1==1802:
                i2_forwarding=0

            #case 17
            # from i1 to rs1 and i1 is R type
            if i1==1701:
                i1_forwarding=-1
                i2_forwarding=505

            #case 18
            # from i1 to rs2 and i1 is lw/jal/jalr type
            if i1==1801:
                i1_forwarding = -1
                i2_forwarding = 505

            return [i1_forwarding,i2_forwarding]

        # if i2 is going to both rs1 and rs2:-
        if i2==1703:
            i1_forwarding=-1
            i2_forwarding=310
            return [i1_forwarding, i2_forwarding]

        #case 18:
        #if i2 is going to rs1:-
        if i2==1801:

            # only dependant on i2 and not i1 (or i2 is given prefrence)
            if i1 == -1 or i1 == 1701 or i1 == 1801:
                i2_forwarding = 21

            #case 17:
            # i1 to rs2:- i1 is R type
            if i1 == 1702:
                i2_forwarding = -1
                i1_forwarding=404

            #case 18:
            # i1 to rs2 , i1 is lw / jal /jalr
            if i1 == 1802:
                i2_forwarding = -1
                i1_forwarding = 404

            return [i1_forwarding,i2_forwarding]

        # if i2 is going to rs2
        if i2 == 1802:

            # only dependant on i2 and not i1 (or i2 is given prefrence)
            if i1 == -1 or i1 == 1702 or i1 == 1802:
                i2_forwarding = 0

            #case 17:
            #i1 to rs1 , i1 is R type :-
            if i1==1701:
                i1_forwarding=-1
                i2_forwarding=505

            #case 18:
            #i1 to rs2 , i1 is lw/jal/jalr type: -
            if i1==1801:
                i1_forwarding=-1
                i2_forwarding=505

            return [i1_forwarding,i2_forwarding]

        # if i2 is going to both rs1 and rs2 : -
        if i2 == 1803:
            i1_forwarding = -1
            i2_forwarding = 505
            return [i1_forwarding, i2_forwarding]

        # case 19
        if i2 == 19:
            i2_forwarding=21
            return [i1_forwarding,i2_forwarding]


        # dealing with cases when there is dependence between i1 and i3 only
        # Case 1
        if i1==103:
            i1_forwarding=13
            return [i1_forwarding,i2_forwarding]
        if i1==102:
            i1_forwarding=12
            return [i1_forwarding,i2_forwarding]
        if i1==101:
            i1_forwarding=11
            return [i1_forwarding,i2_forwarding]
        if i1==1:
            i1_forwarding=11
            return [i1_forwarding,i2_forwarding]

        #Case 2
        if i1==203:
            i1_forwarding=13
            return [i1_forwarding,i2_forwarding]
        if i1==202:
            i1_forwarding=12
            return [i1_forwarding,i2_forwarding]
        if i1==201:
            i1_forwarding=11
            return [i1_forwarding,i2_forwarding]
        if i1==2:
            i1_forwarding=11
            return [i1_forwarding,i2_forwarding]

        #Case 3
        if i1==3:
            i1_forwarding=11
            return [i1_forwarding,i2_forwarding]

        #Case 4: None



        #Case 6 : None


        # Case 8: None

        #Case 9
        if i1 == 9:
            i2_forwarding = -1
            i1_forwarding = 404
            return [i1_forwarding, i2_forwarding]


        #Case 13
        if i1==13:
            i2_forwarding = -1
            i1_forwarding = 404
            return [i1_forwarding, i2_forwarding]

        #Case 17
        if i1==1701:
            i2_forwarding=-1
            i1_forwarding=11
            return [i1_forwarding, i2_forwarding]

        if i1==1702:
            i2_forwarding = -1
            i1_forwarding = 404
            return [i1_forwarding, i2_forwarding]

        if i1==1703:
            i2_forwarding = -1
            i1_forwarding = 404
            return [i1_forwarding, i2_forwarding]

        # case 18
        if i1==1801:
            i2_forwarding = -1
            i1_forwarding = 11
            return [i1_forwarding, i2_forwarding]

        if i1==1802:
            i2_forwarding = -1
            i1_forwarding = 404
            return [i1_forwarding, i2_forwarding]

        if i1==1803:
            i2_forwarding = -1
            i1_forwarding = 404
            return [i1_forwarding, i2_forwarding]

        #case 19:
        if i1 == 19:
            i1_forwarding=11
            return [i1_forwarding,i2_forwarding]


        return [-1,-1] # if no case matches

    def data_stalling(self,i1,i2):

        stall=-1

        # dependency with i2
        # Case1
        if i2 == 103 or i2 == 101 or i2 == 102 or i2 == 1:
            stall = 2
            return stall

        # case2
        if i2 == 203 or i2 == 202 or i2 == 201 or i2 == 2:
            stall = 2
            return stall

        # case3
        if i2 == 3:
            stall = 2
            return stall



        # case9
        if i2 == 9:
            stall = 2
            return stall


        #case13
        if i2 == 13:
            stall = 2
            return stall



        #case17
        if i2 == 1703 or i2==1702 or i2==1701:
            stall = 2
            return stall

        #case18
        if i2 == 1803 or i2==1802 or i2==1801:
            stall = 2
            return stall



        #case19
        if i2 == 19:
            stall = 2
            return stall


        # dependency with i1:-
        # Case1
        if i1 == 103 or i1 == 101 or i1 == 102 or i1 == 1:
            stall = 1
            return stall

        # case2
        if i1 == 203 or i1 == 202 or i1 == 201 or i1 == 2:
            stall = 1
            return stall

        # case3
        if i1 == 3:
            stall = 1
            return stall



        # case9
        if i1 == 9:
            stall = 1
            return stall


        #case13
        if i1 == 13:
            stall = 1
            return stall



        #case17
        if i1 == 1703 or i1==1702 or i1==1701:
            stall = 1
            return stall

        #case18
        if i1 == 1803 or i1==1802 or i1==1801:
            stall = 1
            return stall



        #case19
        if i1 == 19:
            stall = 1
            return stall





        return -1 #if no case matches return stall=-1


    def check_dependence(self, opcode,funct3,rs1,rs2,rd):
        #add data dependence check via registers
        i2=self.current_list[-1]   # this will contain the attributes of the function which was just before the current instruction
        i1=self.current_list[0]   # this will contain the attributes of the function which was
        dependency_i1=-1
        dependency_i2=-1


        #Case2:
        if i2[0]==3 or i2[0]==111 or i2[0]==103:
            if opcode==51:
                if rs1 == i2[4] and rs2 == i2[4]:    # if rs1 or rs2 == to the register where value is being loaded
                    dependency_i2=203
                elif rs1 == i2[4]:    # if rs1 or rs2 == to the register where value is being loaded
                    dependency_i2=201
                elif rs2 == i2[4]:    # if rs1 or rs2 == to the register where value is being loaded
                    dependency_i2=202                   # In case we have a r type instruction just after load.
        if i2[0]==3 or i2[0]==111 or i2[0]==103:            # i2 is load and i3 is I type
            if opcode==19:
                if rs1==i2[4]:
                    dependency_i2=2





        if i1[0]==3 or i1[0]==103 or i1[0]==111:                # i1 is load and i3 is R type
            if opcode==51:
                if rs1 == i1[4] and rs2 == i1[4]:    # if rs1 or rs2 == to the register where value is being loaded
                    dependency_i1=203
                elif rs1 == i1[4]:    # if rs1 or rs2 == to the register where value is being loaded
                    dependency_i1=201
                elif rs2 == i1[4]:    # if rs1 or rs2 == to the register where value is being loaded
                    dependency_i1=202                   # In case we have a r type instruction just after load.

        if i1[0]==3 or i1[0]==103 or i1[0]==111:            # i1 is load and i3 is I type
            if opcode==19:
                if rs1==i1[4]:
                    dependency_i1=2





        #odd Cases
        #Case1
        if i2[0]==51 or i2[0]==19 or i2[0]==23 or i2[0]==55:
            if opcode==51:
                if rs1==i2[4] and rs2==i2[4]:
                    dependency_i2=103
                elif rs1==i2[4]:
                    dependency_i2=101
                elif rs2==i2[4]:
                    dependency_i2=102

        if i1[0]==51 or i1[0]==19 or i1[0]==23 or i1[0]==55:
            if opcode==51:
                if rs1==i1[4] and rs2==i1[4]:
                    dependency_i1=103
                elif rs1==i1[4]:
                    dependency_i1=101
                elif rs2==i1[4]:
                    dependency_i1=102

        if i2[0]==51 or i2[0]==19 or i2[0]==23 or i2[0]==55:
            if opcode==19:
                if rs1==i2[4]:
                    dependency_i2=1
        if i1[0]==51 or i1[0]==19 or i1[0]==23 or i1[0]==55:
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




        #Case9
        if i2[0]==3 or i2[0]==103 or i2[0]==111 or i2[0]==51 or i2[0]==19 or i2[0]==23 or i2[0]==55:
            if opcode==99:
                if rs1==i2[4] or rs2==i2[4]:
                    dependency_i2=9
        if i1[0]==3 or i1[0]==103 or i1[0]==111 or i1[0]==51 or i1[0]==19 or i1[0]==23 or i1[0]==55:
            if opcode==99:
                if rs1==i1[4] or rs2==i1[4]:
                    dependency_i1=9



        #Case13:
        if i2[0]==3 or i2[0]==103 or i2[0]==111 or i2[0]==51 or i2[0]==19 or i2[0]==23 or i2[0]==55:
            if opcode==103:
                if rs1==i2[4]:
                    dependency_i2=13
        if i1[0]==3 or i1[0]==103 or i1[0]==111 or i1[0]==51 or i1[0]==19 or i1[0]==23 or i1[0]==55:
            if opcode==103:
                if rs1==i1[4]:
                    dependency_i1=13


        #Case17:
        if i2[0]==51 or i2[0]==19 or i2[0]==23 or i2[0]==55:
            if opcode==35:
                if rs1==i2[4] and rs2==i2[4]:
                    dependency_i2=1703
                elif rs1==i2[4]:
                    dependency_i2=1701
                elif rs2==i2[4]:
                    dependency_i2=1702

        if i1[0]==51 or i1[0]==19 or i1[0]==23 or i1[0]==55:
            if opcode==35:
                if rs1==i1[4] and rs2==i1[4]:
                    dependency_i1=1703
                elif rs1==i1[4]:
                    dependency_i1=1701
                elif rs2==i1[4]:
                    dependency_i1=1702


        #Case18:
        if i2[0]==3 or i2[0]==103 or i2[0]==111:
            if opcode==35:
                if rs1==i2[4] and rs2==i2[4]:
                    dependency_i2=1803
                elif rs1==i2[4]:
                    dependency_i2=1801
                elif rs2==i2[4]:
                    dependency_i2=1802

        if i1[0]==3 or i1[0]==103 or i1[0]==111:
            if opcode==35:
                if rs1==i1[4] and rs2==i1[4]:
                    dependency_i1=1803
                elif rs1==i1[4]:
                    dependency_i1=1801
                elif rs2==i1[4]:
                    dependency_i1=1802


        #Case19
        if i2[0]==3 or i2[0]==111 or i2[0]==103:
            if opcode==3:
                if rs1==i2[4]:
                    dependency_i2=19
        if i1[0]==3 or i1[0]==111 or i1[0]==103:
            if opcode==3:
                if rs1==i1[4]:
                    dependency_i1=19





        if i1[4]==0:  # rd of i1 is x0 i.e. no dependency
            dependency_i1=-1
        if i2[4]==0:  # rd of i2 is x0 i.e. no dependency
            dependency_i2=-1
        return [dependency_i1,dependency_i2]


    def decision_maker(self,opcode,funct3,rs1,rs2,rd,forwarding_knob):    # if forwarding_knob is 1 then forwarding is on

        dependencies=self.check_dependence(opcode,funct3,rs1,rs2,rd)

        if forwarding_knob == 1:
            ret_value=self.data_forwarding(dependencies[0],dependencies[1])
            print(f"Data Hazard code: {ret_value}")
            return ret_value

        if forwarding_knob == 0:
            #print(f"dependencies- {dependencies[0]} {dependencies[1]}")
            ret_value=self.data_stalling(dependencies[0],dependencies[1])
            print(f"Data Hazard code: {ret_value}")
            return ret_value



    def print_table(self):
        print(self.current_list[0])
        print(self.current_list[1])

    def add_table_inst(self, opcode, funct3, rs1, rs2, rd):
        inst_temp = [opcode, funct3, rs1, rs2, rd]
        self.inst_table.append(inst_temp)

    def print_inst_table(self):
        for i in self.inst_table:
            print(i)

    def count_data_hazards(self):  #[opcode, funct3, rs1, rs2, rd]
        i=0
        count=0
        #dependence1 = False
        while self.inst_table[i][0] != 0x11:
            opcode = self.inst_table[i][0]
            funct3 = self.inst_table[i][1]
            rs1 = self.inst_table[i][2]
            rs2 = self.inst_table[i][3]
            rd = self.inst_table[i][4]

            if i>=1: #check between i2, i3

                if (rs1 != 0 and self.inst_table[i-1][4] == rs1) or (rs2 != 0 and self.inst_table[i-1][4] == rs2):
                    count = count+1
                    #dependence1 = True;

            if i>=2:
                if(self.inst_table[i-1][4] != self.inst_table[i-2][4]):
                    if (rs1 != 0 and self.inst_table[i-2][4] == rs1) or (rs2 != 0 and self.inst_table[i-2][4] == rs2):
                        count = count + 1

            i=i+1
        return count


#current=Current()
#current.add_inst(1, 2, 3, 4, 5)
#current.print_table()
#current.add_null()
#current.print_table()
