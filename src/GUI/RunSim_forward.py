#!/usr/bin/python3
# this file contains code for the simulator. Contains the ALU
from Registers import Registers as reg # contains 32 GP registers and IR
# from Memory import ProcessorMemoryInterface# processor memory interface
from TwoLevelMemory import ProcessorMemoryInterface# processor memory interface
from ControlCircuit_piped import ControlModule # generates control signals
from IAG import InstructionAddressGenerator
from ALU import ArithmeticLogicUnit
from Buffers import Buffers
from Hazard import HazardUnit


MAX_SIGNED_NUM=0x7fffffff
MIN_SIGNED_NUM=-0x80000000
MAX_UNSIGNED_NUM=0xffffffff
MIN_UNSIGNED_NUM=0x00000000
registers=reg() # register object
memory=ProcessorMemoryInterface()
control_module=ControlModule()
ALUmodule=ArithmeticLogicUnit()
IAGmodule=InstructionAddressGenerator()
buffer=Buffers()
hazard_module=HazardUnit()

# Muxes
MuxAout=0 # input 1 of ALU
MuxBout=0 # input 2 of ALU
MuxYout=0 # output of MuxY


class ControlBooleans:
    def __init__(self):
        self.MtoEtoRA=False # booleans to indicate data forwarding in the end of the same cycle, then set it to false
        self.MtoEtoRB=False
        self.EtoEtoRA=False
        self.EtoEtoRB=False
        self.MtoM=False # this is always to MDR(rs2)
        self.decode_stall=False
        self.fetch_stall=False
        self.execute_stall=False
        self.branch_prediction=False
        self.global_terminate=False
        self.control_hazard_cnt=0
        self.load_store=0
        self.total_inst=0
        self.ALU_ins_cnt=0
        self.control_inst=0
        self.bubbles=0
        self.branch_mis_cnt=0
        self.data_stall=0
        self.control_stall=0

forward_bool = ControlBooleans()


def fetch(stage,clock):
    # to do here
    # if terminate==1, return
    control_module.controlStateUpdate(0)
    if(control_module.terminate):
        return
    if not control_module.fetch_deque_signal():
        return
    # operation queue will be used in the buffer update stage, not here.
    # fetch the instruction using the value in PC
    forward_bool.global_terminate=False
    buffer.IRbuffer=memory.LoadInstruction(IAGmodule.PC) # update IR buffer
    forward_bool.branch_prediction=IAGmodule.BTB_check(IAGmodule.PC)# update branch prediction
    target_obj=-1
    if forward_bool.branch_prediction:
        target_obj=IAGmodule.BTB[IAGmodule.PC]
        buffer.Fetch_output_PC_temp=target_obj.target_address
        print(f"Fetch- Branch prediction.{buffer.Fetch_output_PC_temp} predicted")
    else:
        buffer.Fetch_output_PC_temp=IAGmodule.PC+4
    # compare it to BTB to check if that is a branch/jump. If it is, update PC to the target.
    

def decode(stage,clock):
    # if terminate==1, return
    # check the operation queue. If empty, then operate. Else, don't operate and pop.
    if(control_module.terminate):
        hazard_module.add_table_inst(0x11,0,0,0,0)
        return
    forward_bool.global_terminate=False
    print("Decode Stage")
    if not (control_module.decode_deque_signal()):
        # decode stage is inactive. Perform other tasks
        if control_module.MtoEcode==0: # decode init
            forward_bool.decode_stall=True
            return
        if control_module.MtoEcode==-2: # branch misprediction
            forward_bool.fetch_stall=False
            forward_bool.decode_stall=True
            return
        forward_bool.decode_stall=True
        forward_bool.fetch_stall=True
        if control_module.MtoEcode==21:
            forward_bool.data_stall+=1
            forward_bool.execute_stall=True
            forward_bool.MtoEtoRA=True
            return
        if control_module.MtoEcode==22:
            forward_bool.data_stall+=1
            forward_bool.execute_stall=True
            forward_bool.MtoEtoRB=True
            return
        if control_module.MtoEcode==23:
            forward_bool.data_stall+=1
            forward_bool.execute_stall=True
            forward_bool.MtoEtoRA=True
            forward_bool.MtoEtoRB=True
            return
    
    # decode the instruction first in the IR
    control_module.decode(registers.ReadIR(),buffer.Decode_input_PC)
    if control_module.terminate:
        return
    # check for hazards using the hazard table.
    hazard_code=hazard_module.decision_maker(control_module.opcode, control_module.funct3, control_module.rs1, control_module.rs2, control_module.rd, 1) # 1 for forwarding
    # if hazard, perform corrective measures here and return. Do not execute further code
    to_return=False
    if hazard_code[1]!=-1 or hazard_code[0]!=-1: # data hazard!
        print(f"Hazard-{buffer.Decode_input_PC}")
        # code here for data hazard
        # first handling hazard[0] then hazard[1]
        if hazard_code[1]!=-1:
            if hazard_code[1]==404: # 1 decode stall
                print("Decode stall")
                control_module.execute_set_NOP()
                control_module.memory_set_NOP()
                control_module.register_set_NOP()
                forward_bool.decode_stall=True
                forward_bool.fetch_stall=True
                forward_bool.data_stall+=1
                to_return=True
            elif hazard_code[1]==505: # 2 decode stall
                print("Decode stall")
                control_module.execute_set_NOP()
                control_module.memory_set_NOP()
                control_module.register_set_NOP()
                forward_bool.decode_stall=True
                forward_bool.fetch_stall=True
                forward_bool.data_stall+=1
                to_return=True
            if hazard_code[1]==310:
                control_module.mem_ForwardingQueue.append(0) # set boolean to true in memory module
                print("MyoM, EtoEtoRA")
                forward_bool.EtoEtoRA=True
            elif hazard_code[1]==0:
                control_module.mem_ForwardingQueue.append(0) # set boolean to true in memory module
            elif hazard_code[1]==11:
                print("MtoEtoRA")
                forward_bool.MtoEtoRA=True
            elif hazard_code[1]==12:
                forward_bool.MtoEtoRB=True
            elif hazard_code[1]==13:
                forward_bool.MtoEtoRA=True
                forward_bool.MtoEtoRB=True
            elif hazard_code[1]==21:
                control_module.decode_operation.append(21)
                # push 1 nop and the decoded instruction in the queues
                control_module.execute_set_NOP()
                control_module.memory_set_NOP()
                control_module.register_set_NOP()
            elif hazard_code[1]==22:
                control_module.decode_operation.append(22)
                control_module.execute_set_NOP()
                control_module.memory_set_NOP()
                control_module.register_set_NOP()
            elif hazard_code[1]==23:
                control_module.decode_operation.append(23)
                #control_module.decode_set_NOP() # edit
                # push 1 nop and the decoded instruction in the queues
                control_module.execute_set_NOP()
                control_module.memory_set_NOP()
                control_module.register_set_NOP()
            elif hazard_code[1]==31:
                print("EtoEtoRA")
                forward_bool.EtoEtoRA=True
            elif hazard_code[1]==32:
                print("EtoEtoRB")
                forward_bool.EtoEtoRB=True
            elif hazard_code[1]==33:
                print("EtoEtoRB RA")
                forward_bool.EtoEtoRA=True
                forward_bool.EtoEtoRB=True
            
        if hazard_code[0]!=-1:
            if hazard_code[0]==404:
                print("Decode stall")
                control_module.execute_set_NOP()
                control_module.memory_set_NOP()
                control_module.register_set_NOP()
                forward_bool.decode_stall=True
                forward_bool.fetch_stall=True
                forward_bool.data_stall+=1
                to_return=True
            elif hazard_code[0]==505:
                print("Decode stall")
                control_module.execute_set_NOP()
                control_module.memory_set_NOP()
                control_module.register_set_NOP()
                forward_bool.decode_stall=True
                forward_bool.fetch_stall=True
                forward_bool.data_stall+=1
                to_return=True
            elif hazard_code[0]==310:
                control_module.mem_ForwardingQueue.append(0) # set boolean to true in memory module
                print("MtoM, EtoEtoRA")
                forward_bool.EtoEtoRA=True
            elif hazard_code[0]==0:
                control_module.mem_ForwardingQueue.append(0) # set boolean to true in memory module
            elif hazard_code[0]==11:
                print("MtoEtoRA")
                forward_bool.MtoEtoRA=True
            elif hazard_code[0]==12:
                forward_bool.MtoEtoRB=True
            elif hazard_code[0]==13:
                forward_bool.MtoEtoRA=True
                forward_bool.MtoEtoRB=True
            elif hazard_code[0]==21:
                control_module.decode_operation.append(21)
                control_module.execute_set_NOP()
                control_module.memory_set_NOP()
                control_module.register_set_NOP()
            elif hazard_code[0]==22:
                control_module.decode_operation.append(22)
                control_module.execute_set_NOP()
                control_module.memory_set_NOP()
                control_module.register_set_NOP()
            elif hazard_code[0]==23:
                control_module.decode_operation.append(23)
                control_module.execute_set_NOP()
                control_module.memory_set_NOP()
                control_module.register_set_NOP()
            elif hazard_code[0]==31:
                forward_bool.EtoEtoRA=True
            elif hazard_code[0]==32:
                forward_bool.EtoEtoRB=True
            elif hazard_code[0]==33:
                forward_bool.EtoEtoRA=True
                forward_bool.EtoEtoRB=True
           
    if to_return:
        return
    # check for branch misprediction here, use Decode_input_branch_prediction
    # read the registers or PC or forwarded value here and update RA and RB with those values. Use control signals for MuxA and MuxB to set them!!!!
    
    ########## reading the registers#############
    MuxAout=0
    MuxBout=0
    if control_module.MuxBSelect==0:
        MuxBout=registers.ReadGpRegisters(control_module.rs2)
    elif control_module.MuxBSelect==1:
        MuxBout=control_module.imm
    if control_module.MuxASelect==0:
        MuxAout=registers.ReadGpRegisters(control_module.rs1)
    elif control_module.MuxASelect==1:
        MuxAout=buffer.Decode_input_PC
    # code for executing ALU for branch misprediction here.
    buffer.RAtemp=MuxAout
    buffer.RBtemp=MuxBout
    buffer.RMtemp=registers.ReadGpRegisters(control_module.rs2)
    control_module.RM_placeholder=buffer.RMtemp
    control_module.RA_placeholder=buffer.Decode_input_PC+4 # return address
    ALUmodule.outputBool=0
    if control_module.branch:
        forward_bool.ALU_ins_cnt+=1
        ALUmodule.ALUexecute(control_module.ALUOp, control_module.ALUcontrol, buffer.RAtemp, buffer.RBtemp)
    IAGmodule.PC_buffer=buffer.Decode_input_PC
    control_module.branching_controlUpdate(ALUmodule.outputBool)
    IAGmodule.PCset(buffer.RAtemp, control_module.MuxPCSelect)
    IAGmodule.SetBranchOffset(control_module.imm)
    IAGmodule.PCUpdate(control_module.MuxINCSelect) # value in PC_buffer
    #print(f"\t\t\tiag pc buffer {hex(IAGmodule.PC_buffer)}")
    #buffer.Decode_output_PC_temp=IAGmodule.PC_buffer
    # use branch prediction from the buffer
    #print(f"RAtemp-{buffer.RAtemp} RBtemp-{buffer.RBtemp} RA-{buffer.RA} RB-{buffer.RB}")
    #print(f"\t\t\tRA placeholder- {control_module.RA_placeholder}")
    control_module.branch_misprediction=buffer.Decode_input_branch_prediction^(control_module.jump or (control_module.branch and ALUmodule.outputBool))

    if buffer.Decode_input_branch_prediction==0 and (control_module.opcode==111):
        print(f"BTB entry created. {IAGmodule.PC_buffer}")
        IAGmodule.BTB_insert(buffer.Decode_input_PC,IAGmodule.PC_buffer,1)

    if buffer.Decode_input_branch_prediction==0 and control_module.branch:
        print(f"BTB entry created. {buffer.Decode_input_PC+control_module.imm}")
        IAGmodule.BTB_insert(buffer.Decode_input_PC,buffer.Decode_input_PC+control_module.imm,1)

    if control_module.branch_misprediction: 
        # code here for handling branch misprediction
        print("Branch misprediction")
        forward_bool.branch_mis_cnt+=1
        forward_bool.control_stall+=1
        forward_bool.control_hazard_cnt+=1
        control_module.decode_operation.append(-2) # -2 is the code to indicate a branch misprediction and the decode unit does not have to operate
        forward_bool.total_inst+=1
        if control_module.jump or control_module.branch:
            forward_bool.control_inst+=1
        hazard_module.add_inst(control_module.opcode, control_module.funct3, control_module.rs1, control_module.rs2, control_module.rd)
        hazard_module.add_table_inst(control_module.opcode, control_module.funct3, control_module.rs1, control_module.rs2, control_module.rd) # end of prog
        buffer.Decode_output_PC_temp=IAGmodule.PC_buffer
        control_module.execute_set_operate()
        control_module.memory_set_operate()
        control_module.register_set_operate()
        control_module.execute_set_NOP()
        control_module.memory_set_NOP()
        control_module.register_set_NOP()
        return 
    # push NOPs whenever needed, call the exexute_set_NOP etc methods is ControlModule according to hazard code
    # if misprediction, perform corrective measures here and return if necessary follow steps given in documentation to resolve the hazard by stalling/data forwarding.
    # in case of jalr, compute effective address and update decode_output_PC_temp by that value.
    # if all good, push the decoded the signals into the queues.
    forward_bool.total_inst+=1
    if control_module.jump or control_module.branch:
            forward_bool.control_inst+=1
    hazard_module.add_inst(control_module.opcode, control_module.funct3, control_module.rs1, control_module.rs2, control_module.rd)
    hazard_module.add_table_inst(control_module.opcode, control_module.funct3, control_module.rs1, control_module.rs2, control_module.rd) # end of prog
    control_module.execute_set_operate()
    control_module.memory_set_operate()
    control_module.register_set_operate()

def execute(stage,clock): # ALU
    # dequeue from the control signals. Check if we need to operate or not
    if not control_module.execute_deque_signal(): # this function returns False if memory is in NOP. Also, all control_module.ALUop, etc are updated to 0 in case of NOP, or correct value if OP
        # perform other tasks and return
        return
    forward_bool.global_terminate=False
    print("Execute Stage")
    # can use control_module.ALUop etc directly to use as arguments to ALU.
    #print(f"ALUcontrol-{control_module.ALUcontrol} ALUop-{control_module.ALUOp}")
    if control_module.ALUOp:
        forward_bool.ALU_ins_cnt+=1
    ALUmodule.ALUexecute(control_module.ALUOp, control_module.ALUcontrol,buffer.getRA(), buffer.getRB())
    buffer.RZtemp=ALUmodule.output32	#simple execution
    #print(f"clock- {clock} RZtemp-{buffer.RZtemp} ALUoutput-{ALUmodule.output32}")
    
    
def mem_access(stage,clock):
    # dequeue from the control signals. Check if we need to operate or not
    if not control_module.memory_deque_signal(): # this function returns False if memory is in NOP. Also, all control_module.MemRead, etc are updated to 0 in case of NOP, or correct value if O
      # perform other tasks and return
        return
    forward_bool.global_terminate=False
    print("Memory Access")
    # acess memory and update temp memory buffers (RM_temp)
    # check forwarding
    if memory.take_from_rm:
        print("Taken from M")
        control_module.RM_placeholder=buffer.RM
        memory.take_from_rm=False
    if control_module.MemRead or control_module.MemWrite:
        forward_bool.load_store+=1
    memory.AccessMemory(control_module.MemRead, control_module.MemWrite, buffer.getRZ(), control_module.BytesToAccess, control_module.RM_placeholder) # why RMtemp? RM is updated at the end of cycle
    #print(f"Memory MDR- {memory.MDR} Memory MAR- {memory.MAR}")
    if len(control_module.mem_ForwardingQueue) != 0:
      # check forwarding code
      # if MtoE
        control_module.MtoEcode=control_module.mem_ForwardingQueue.popleft() # m to m forwarding
        if control_module.MtoEcode==0:
            forward_bool.MtoM = True
            memory.take_from_rm=True
        elif control_module.MtoEcode==21:
            forward_bool.MtoEtoRA=True
            forward_bool.MtoEtoRB=False
        elif control_module.MtoEcode==22:
            forward_bool.MtoEtoRB=True
            forward_bool.MtoEtoRA=False
        elif control_module.MtoEcode==23:
            forward_bool.MtoEtoRA=True
            forward_bool.MtoEtoRB=True
    
      # make MtoEToRA or MtoEtoRB true on the basis of encoding received
      # if MtoM
    if control_module.MuxYSelect == 0:
        #print("RZ to RY")
        buffer.RYtemp = buffer.getRZ()
    elif control_module.MuxYSelect == 1:
        #print(f"MDR to RY {memory.MDR}")
        buffer.RYtemp = memory.MDR
    elif control_module.MuxYSelect == 2:
        #print(f"\t\tRY set to RA!! {control_module.RA_placeholder}")
        buffer.RYtemp = control_module.RA_placeholder

def reg_writeback(stage,clock):
    # dequeue from the control signals. Check if we need to operate or not
    if not control_module.register_deque_signal(): # this function returns False if reg_write_back is in NOP. Also, all control_module.ALUop, etc are updated to 0 in case of NOP, or correct value if OP
        # perform other tasks and return
        return
    forward_bool.global_terminate=False
    print("RegisterWrite stage")
    registers.WriteGpRegisters(control_module.rd, control_module.RegWrite, buffer.getRY())

def buffer_update():
    #first update the output buffers, 
    #then forward   
    #temp to Buffer data transfer
    if not forward_bool.fetch_stall:
        registers.WriteIR(buffer.IRbuffer,1)
        buffer.Decode_input_branch_prediction=forward_bool.branch_prediction
        buffer.Decode_input_PC=IAGmodule.PC
        if not control_module.branch_misprediction:
            print(f"PC updated by fetch {buffer.Fetch_output_PC_temp}")
            IAGmodule.PC=buffer.Fetch_output_PC_temp
    if not forward_bool.decode_stall:
        buffer.RA=buffer.RAtemp
        buffer.RB=buffer.RBtemp

        if control_module.branch_misprediction:
            print(f"PC updated by decode {IAGmodule.PC_buffer}")

            IAGmodule.PC=IAGmodule.PC_buffer
    if not forward_bool.execute_stall: 
        buffer.RZ=buffer.RZtemp	#RZ update

    buffer.RY=buffer.RYtemp
      #forward data in priority
    if forward_bool.MtoM:
        
        # RM is updated to MDR of memory in case of M to M forwarding
        buffer.RM=buffer.RY
        forward_bool.MtoM = False
      
    if forward_bool.MtoEtoRA:	#MDR to RA
        buffer.RA=buffer.RY
        forward_bool.MtoEtoRA = False
        
    if forward_bool.MtoEtoRB:	#MDR to RB
        buffer.RB=buffer.RY
        forward_bool.MtoEtoRB = False
        
    if forward_bool.EtoEtoRA:	#RZ to RA(rs1)
        print("E to E to RA")
        buffer.RA=buffer.RZ
        forward_bool.EtoEtoRA = False
        
    if forward_bool.EtoEtoRB:	#RZ to RB(rs2)
        buffer.RB=buffer.RZ
        forward_bool.EtoEtoRB = False
    
    
    if forward_bool.fetch_stall or forward_bool.decode_stall or forward_bool.execute_stall:
        hazard_module.add_null()

    forward_bool.fetch_stall = False

    forward_bool.decode_stall = False

    forward_bool.execute_stall = False

    control_module.branch_misprediction=False
    # print(f"RZ update, temp-{buffer.RZtemp}, RZ-{buffer.RZ}")
    # print(f"buff update- RAtemp-{buffer.RAtemp} RBtemp-{buffer.RBtemp} RA-{buffer.RA} RB-{buffer.RB}")
    # print(f"execute queue- aluop {control_module.exe_ALUOp} aluc {control_module.ALUcontrol} opcode {control_module.exe_opcode}") 

clock=0     
def RunSim(reg_print=1, buffprint=1):
    global clock
    if forward_bool.global_terminate:
        return
    while(True):
        clock=clock+1
        print(f"\n\033[1;96mCycle {clock}\033[0m")
        forward_bool.global_terminate=True
        reg_writeback(4, clock)
        mem_access(3,clock)
        execute(2,clock)
        print("Hazard Table:")
        hazard_module.print_table()
        decode(1,clock)
        fetch(0,clock)
        buffer_update()
        #print(f"PC{(IAGmodule.PC)} IR {hex(registers.IR)} RZ {buffer.RZ} RY {buffer.RY}\n###########################################\n")
        if reg_print==1:
            print("Register file: ")
            for i in range(32):
                print(f"reg[{i}]={hex(registers.reg[i]) }",end=" ")
                if i%8==0 and i>0:
                    print()
        print()
        if buffprint==1:
            print("Pipeline buffers: ")
            print(f"\033[1;96mPC: {hex(IAGmodule.PC)} IR: {hex(registers.IR)} RZ: {buffer.RZ} RY: {buffer.RY}\nRA: {buffer.RA} RB: {buffer.RB} Decode-Input-PC: {buffer.Decode_input_PC}\nBranch prediction buffer: {buffer.Decode_input_branch_prediction}\033[0m")
        print("##################################################")
        if forward_bool.global_terminate:
            print("\033[1;92m\nProgram Terminated Successfully\033[0m")
            print("Stats-")
            print(f"Stat1: Cycles: {clock}")
            print(f"Stat2: Total Instructions: {forward_bool.total_inst}")
            print(f"Stat3: CPI: {clock/forward_bool.total_inst}")
            print(f"Stat4: Load/Store: {forward_bool.load_store} ")
            print(f"Stat5: ALU instructions: {forward_bool.ALU_ins_cnt} ")
            print(f"Stat6: Control instructions: {forward_bool.control_inst} ")
            print(f"Stat7: Bubbles: {forward_bool.data_stall+forward_bool.control_stall}")
            tot_data_hazards=hazard_module.count_data_hazards()
            print(f"Stat8: Total Data Hazards: {tot_data_hazards}")
            print(f"Stat9: Total Control Hazards: {forward_bool.control_hazard_cnt}")
            print(f"Stat10: Total branch mispredictions: {forward_bool.branch_mis_cnt}")
            print(f"Stat11: Stalls due to data hazard: {forward_bool.data_stall}")
            print(f"Stat12: Stalls due to control hazard: {forward_bool.control_stall}")
            stats=[clock, forward_bool.total_inst, clock/forward_bool.total_inst, forward_bool.load_store,
            forward_bool.ALU_ins_cnt, forward_bool.control_inst, forward_bool.data_stall+forward_bool.control_stall,
            tot_data_hazards, forward_bool.control_hazard_cnt, forward_bool.branch_mis_cnt, forward_bool.data_stall, forward_bool.control_stall]
            print("Cache Stats-")
            print("I$: ")
            print(f"Total Accesses: {memory.text_module.cache_accesses}")
            print(f"Total Hits: {memory.text_module.cache_hits}")
            print(f"Total Miss: {memory.text_module.cache_miss}")
            print("D$: ")
            print(f"Total Accesses: {memory.data_module.cache_accesses}")
            print(f"Total Hits: {memory.data_module.cache_hits}")
            print(f"Total Miss: {memory.data_module.cache_miss}")
            return stats

def RunSim_step(reg_print=1, buffprint=1):
    global clock
    if forward_bool.global_terminate:
        return
    clock=clock+1
    print(f"\n\033[1;96mCycle {clock}\033[0m")
    forward_bool.global_terminate=True
    reg_writeback(4, clock)
    mem_access(3,clock)
    execute(2,clock)
    print("Hazard Table:")
    hazard_module.print_table()
    decode(1,clock)
    fetch(0,clock)
    buffer_update()
    if reg_print==1:
        print("Register file: ")
        for i in range(32):
            print(f"reg[{i}]={hex(registers.reg[i]) }",end=" ")
            if i%8==0 and i>0:
                print()
    print()
    if buffprint==1:
        print("Pipeline buffers: ")
        print(f"\033[1;96mPC: {hex(IAGmodule.PC)} IR: {hex(registers.IR)} RZ: {buffer.RZ} RY: {buffer.RY}\nRA: {buffer.RA} RB: {buffer.RB} Decode-Input-PC: {buffer.Decode_input_PC}\nBranch prediction buffer: {buffer.Decode_input_branch_prediction}\033[0m")
    print("##################################################")
    if forward_bool.global_terminate:
        print("\033[1;92m\nProgram Terminated Successfully\033[0m")
        print("Stats-")
        print(f"Stat1: Cycles: {clock}")
        print(f"Stat2: Total Instructions: {forward_bool.total_inst}")
        print(f"Stat3: CPI: {clock/forward_bool.total_inst}")
        print(f"Stat4: Load/Store: {forward_bool.load_store} ")
        print(f"Stat5: ALU instructions: {forward_bool.ALU_ins_cnt} ")
        print(f"Stat6: Control instructions: {forward_bool.control_inst} ")
        print(f"Stat7: Bubbles: {forward_bool.data_stall+forward_bool.control_stall}")
        tot_data_hazards=hazard_module.count_data_hazards()
        print(f"Stat8: Total Data Hazards: {tot_data_hazards}")
        print(f"Stat9: Total Control Hazards: {forward_bool.control_hazard_cnt}")
        print(f"Stat10: Total branch mispredictions: {forward_bool.branch_mis_cnt}")
        print(f"Stat11: Stalls due to data hazard: {forward_bool.data_stall}")
        print(f"Stat12: Stalls due to control hazard: {forward_bool.control_stall}")
        stats=[clock, forward_bool.total_inst, clock/forward_bool.total_inst, forward_bool.load_store,
        forward_bool.ALU_ins_cnt, forward_bool.control_inst, forward_bool.data_stall+forward_bool.control_stall,
        tot_data_hazards, forward_bool.control_hazard_cnt, forward_bool.branch_mis_cnt, forward_bool.data_stall, forward_bool.control_stall]
        print("Cache Stats-")
        print("I$: ")
        print(f"Total Accesses: {memory.text_module.cache_accesses}")
        print(f"Total Hits: {memory.text_module.cache_hits}")
        print(f"Total Miss: {memory.text_module.cache_miss}")
        print("D$: ")
        print(f"Total Accesses: {memory.data_module.cache_accesses}")
        print(f"Total Hits: {memory.data_module.cache_hits}")
        print(f"Total Miss: {memory.data_module.cache_miss}")
        return stats