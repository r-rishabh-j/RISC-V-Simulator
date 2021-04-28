# 3 types of stalls- decode stall, fetch stall and execute stall
# RAW data hazards-
# Case1- between D and 

    #in transit instructions
from collections import deque

# class Current:
class HazardUnit:
    def __init__(self):
        self.current_list = deque([[-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1]])

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
        #case 5 , dependency with i2:-

        # here rd of i2 is both rs1 and rs2 : -
        if i2==503:
            i2_forwarding=33
            return  [i1_forwarding,i2_forwarding]

        # here rd of i2 is related to rs1
        if i2==501:
            i2_forwarding=31

            #Case 5 if i1 is related to rs2
            if i1==502:
                i1_forwarding=12

            #case 10 here always i1 is related to rs2
            if i1==102:
                i1_forwarding=12
            return  [i1_forwarding,i2_forwarding]


        # here rd of i2 is related to rs2
        if i2==502:
            i2_forwarding=32

            # Case 5 if i1 is related to rs1
            if i1==501:
                i1_forwarding=11

            # Case 10 if i1 is related to rs1
            if i1==101:
                i1_forwarding=11

            return  [i1_forwarding,i2_forwarding]
        
        #Case 7 , checking dependency with i2:-

        #rd of i2 is related to both rs1 and rs2
        if i2==703:
            i2_forwarding=63
            return [i1_forwarding,i2_forwarding]

        # rd of i2 is related to rs1
        if i2==701:
            i2_forwarding=61

            # case 7 , i1 to rs2
            if i1==702:
                i1_forwarding=72

            # case 9 , i1 to rs2
            if i1==902:
                i1_forwarding=52
            return [i1_forwarding, i2_forwarding]

        # rd of i2 is related to rs2
        if i2 == 702:
            i2_forwarding=62

            # case 7 , i1 to rs1
            if i1==701:
                i1_forwarding=71

            # case 9 , i1 to rs1
            if i1==901:
                i1_forwarding=51

            return [i1_forwarding,i2_forwarding]
            
        # Case 9 ,checking dependancy with i2:-

        #rd of i2 is related to both rs1 and rs2
        if i2==903:
            i2_forwarding=43
            return [i1_forwarding,i2_forwarding]

        #rd of i2 is related to rs2
        if i2==902:
            i2_forwarding=42

            #case 7 rd of i1 is related to rs1
            if i1==701:
                i1_forwarding=71

            #case 9 rd of i1 is related to rs1
            if i1==901:
                i1_forwarding=51

            return [i1_forwarding,i2_forwarding]

        #rd of i2 is related to rs1
        if i2==901:
            i2_forwarding=41

            #case 7 rd of i1 is related to rs2
            if i1==702:
                i1_forwarding=72

            #case 9 rd of i1 is related to rs2
            if i1==902:
                i1_forwarding=52

            return  [i1_forwarding,i2_forwarding]
            
        # case 10 , checking dependancy with i2

        # from i2 to both rs2 and rs1
        if i2==1003:
            i2_forwarding=23
            return [i1_forwarding,i2_forwarding]

        # from i2 to rs2
        if i2==1002:
            i2_forwarding=0

            #case 10 from i1 to rs1
            if i1==1001:
                i1_forwarding=11

            # case 5 from i1 to rs1
            if i1==501:
                i1_forwarding=11
            return [i1_forwarding,i2_forwarding]

        # from i2 to rs1
        if i2==1001:
            i2_forwarding =21

            #case 10 from i1 to rs2
            if i1==1002:
               i1_forwarding =12

            # case 5 from i1 to rs2
            if i1==502:
                i1_forwarding=12

            return [i1_forwarding,i2_forwarding]

        #case 15, dependency with i2:-

        # here only forwarding to rs1 is possible : -
        if i2==15:
            i2_forwarding=61
            return [i1_forwarding,i2_forwarding]

        if i2==16:
            i2_forwarding=41
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

        #Case 5
        if i1==503:
            i1_forwarding=13
            return [i1_forwarding,i2_forwarding]
        if i1==502:
            i1_forwarding=12
            return [i1_forwarding,i2_forwarding]
        if i1==501:
            i1_forwarding=11
            return [i1_forwarding,i2_forwarding]

        #Case 6 : None
        
        #Case 7
        if i1==703:
            i1_forwarding=73
            return [i1_forwarding,i2_forwarding]
        if i1==702:
            i1_forwarding=72
            return [i1_forwarding,i2_forwarding]
        if i1==701:
            i1_forwarding=71
            return [i1_forwarding,i2_forwarding]
        
        # Case 8: None

        #Case 9
        if i1==903:
            i1_forwarding=53
            return [i1_forwarding,i2_forwarding]
        if i1==902:
            i1_forwarding=52
            return [i1_forwarding,i2_forwarding]
        if i1==901:
            i1_forwarding=51
            return [i1_forwarding,i2_forwarding]
        
        #Case 10
        if i1==1003:
            i1_forwarding=13
            return [i1_forwarding,i2_forwarding]
        if i1==1002:
            i1_forwarding=12
            return [i1_forwarding,i2_forwarding]
        if i1==1001:
            i1_forwarding=11
            return [i1_forwarding,i2_forwarding]


        #Case 15
        if i1==15:
            i1_forwarding=71
            return [i1_forwarding,i2_forwarding]

        #Case 16
        if i1==16:
            i1_forwarding=51
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

        # case5
        if i2 == 503 or i2==501 or i2==502:
            stall = 2
            return stall

        # case7
        if i2 == 701 or i2 == 702 or i2 == 703:
            stall = 2
            return stall

        # case9
        if i2 == 901 or i2 == 903 or i2 == 902:
            stall = 2
            return stall

        # case10
        if i2 == 1001 or i2 == 1002 or i2 == 1003:
            stall = 2
            return stall

        #case15
        if i2 == 15:
            stall = 2
            return stall

        #case16
        if i2 == 16:
            stall = 2
            return stall


        # dependency with i1:-
        #Case1
        if i1==103 or i1==102 or i1==101 or i1==1:
            stall=1
            return stall
        
        #Case2
        if i1==203 or i1==202 or i1==201 or i1==2:
            stall=1
            return stall

        #Case3
        if i1==3:
            stall=1
            return stall

        #Case4:None

        #Case5
        if i1==503 or i1==502 or i1==501:
            stall=1
            return stall


        #Case6:None

        #Case7
        if i1==703 or i1==702 or i1==701:
            stall=1
            return stall
        
        #Case8:None

        #Case9
        if i1==903 or i1==902 or i1==901:
            stall=1
            return stall

        #Case10
        if i1==1003 or i1==1002 or i1==1001:
            stall=1
            return stall

        #Case11,12,13,14

        #Case15
        if i1==15:
            stall=1
            return stall

        #Case16
        if i1==16:
            stall=1
            return stall




        return -1 #if no case matches return stall=-1
            

    def check_dependence(self, opcode,funct3,rs1,rs2,rd):
        #add data dependence check via registers
        i2=self.current_list[-1]   # this will contain the attributes of the function which was just before the current instruction
        i1=self.current_list[0]   # this will contain the attributes of the function which was
        dependency_i1=-1
        dependency_i2=-1

        if i2[0]==3:                # i2 is load and i3 is R type
            if opcode==51:
                if rs1 == i2[4] and rs2 == i2[4]:    # if rs1 or rs2 == to the register where value is being loaded
                    dependency_i2=203
                elif rs1 == i2[4]:    # if rs1 or rs2 == to the register where value is being loaded
                    dependency_i2=201
                elif rs2 == i2[4]:    # if rs1 or rs2 == to the register where value is being loaded
                    dependency_i2=202                   # In case we have a r type instruction just after load.
        if i2[0]==3:            # i2 is load and i3 is I type
            if opcode==19:
                if rs1==i2[4]:
                    dependency_i2=2

        if i2[0] == 3:  # if i2 is load and i3 is store type
            if opcode == 35:
                if i2[4] == rs2 and i2[4]==rs1:   # if the rs2 or source of data is same as rd in load
                    dependency_i2=1003
                elif i2[4]==rs1:   # if the rs2 or source of data is same as rd in load
                    dependency_i2=1001
                elif i2[4] == rs2:   # if the rs2 or source of data is same as rd in load
                    dependency_i2=1002



        if i1[0]==3:                # i1 is load and i3 is R type
            if opcode==51:
                if rs1 == i1[4] and rs2 == i1[4]:    # if rs1 or rs2 == to the register where value is being loaded
                    dependency_i1=203
                elif rs1 == i1[4]:    # if rs1 or rs2 == to the register where value is being loaded
                    dependency_i1=201
                elif rs2 == i1[4]:    # if rs1 or rs2 == to the register where value is being loaded
                    dependency_i1=202                   # In case we have a r type instruction just after load.

        if i1[0]==3:            # i1 is load and i3 is I type
            if opcode==19:
                if rs1==i1[4]:
                    dependency_i1=2

        if i1[0] == 3:  # if i1 is load and i3 is store type
            if opcode == 35:
                if i1[4] == rs2 and i1[4]==rs1:    # if the rs2 or source of data is same as rd in load
                    dependency_i1=1003
                elif i1[4]==rs1:    # if the rs2 or source of data is same as rd in load
                    dependency_i1=1001
                elif i1[4] == rs2:    # if the rs2 or source of data is same as rd in load
                    dependency_i1=1002

        

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

        #Case5
        if i2[0]==51 or i2[0]==19 or i2[0]==23 or i2[0]==55:
            if opcode==35:
                if rs1==i2[4] and rs2==i2[4]:
                    dependency_i2=503
                elif rs1==i2[4]:
                    dependency_i2=501
                elif rs2==i2[4]:
                    dependency_i2=502
        if i1[0]==51 or i1[0]==19 or i1[0]==23 or i1[0]==55:
            if opcode==35:
                if rs1==i1[4] and rs2==i1[4]:
                    dependency_i1=503
                elif rs1==i1[4]:
                    dependency_i1=501
                elif rs2==i1[4]:
                    dependency_i1=502

        #Case7
        if i2[0]==51 or i2[0]==19:
            if opcode==99:
                if rs1==i2[4] and rs2==i2[4]:
                    dependency_i2=703
                elif rs1==i2[4]:
                    dependency_i2=701
                elif rs2==i2[4]:
                    dependency_i2=702
        if i1[0]==51 or i1[0]==19:
            if opcode==99:
                if rs1==i1[4] and rs2==i1[4]:
                    dependency_i1=703
                elif rs1==i1[4]:
                    dependency_i1=701
                elif rs2==i1[4]:
                    dependency_i1=702

        #Case9
        if i2[0]==3:
            if opcode==99:
                if rs1==i2[4] and rs2==i2[4]:
                    dependency_i2=903
                elif rs1==i2[4]:
                    dependency_i2=901
                elif rs2==i2[4]:
                    dependency_i2=902
        if i1[0]==3:
            if opcode==99:
                if rs1==i1[4] and rs2==i1[4]:
                    dependency_i1=903
                elif rs1==i1[4]:
                    dependency_i1=901
                elif rs2==i1[4]:
                    dependency_i1=902

        #Case11

        #Case13:None
        #Case15:
        if i2[0]==51 or i2[0]==19 or i2[0]==23 or i2[0]==55:
            if opcode==103:
                if rs1==i2[4]:
                    dependency_i2=15
        if i1[0]==51 or i1[0]==19 or i1[0]==23 or i1[0]==55:
            if opcode==103:
                if rs1==i1[4]:
                    dependency_i1=15


        #Case16:
        if i2[0]==3:
            if opcode==103:
                if rs1==i2[4]:
                    dependency_i2=16
        if i1[0]==3:
            if opcode==103:
                if rs1==i1[4]:
                    dependency_i1=16
    

        if i1[4]==0:  # rd of i1 is x0 i.e. no dependency
            dependency_i1=-1 
        if i2[4]==0:  # rd of i2 is x0 i.e. no dependency
            dependency_i2=-1
        return [dependency_i1,dependency_i2]


    def decision_maker(self,opcode,funct3,rs1,rs2,rd,forwarding_knob):    # if forwarding_knob is 1 then forwarding is on

        dependencies=self.check_dependence(opcode,funct3,rs1,rs2,rd)

        if forwarding_knob == 1:
            ret_value=self.data_forwarding(dependencies[0],dependencies[1])
            print(f"\t\thazard- decision {ret_value}")
            return ret_value

        if forwarding_knob == 0:
            print(f"dependencies- {dependencies[0]} {dependencies[1]}")
            ret_value=self.data_stalling(dependencies[0],dependencies[1])
            print(f"\t\thazard- decision {ret_value}")
            return ret_value
            


    def print_table(self):
        print(self.current_list[0])
        print(self.current_list[1])


#current=Current()
#current.add_inst(1, 2, 3, 4, 5)
#current.print_table()
#current.add_null()
#current.print_table()


