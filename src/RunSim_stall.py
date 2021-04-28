#!/usr/bin/python3
# this file contains code for the simulator. Contains the ALU
from Registers import Registers as reg # contains 32 GP registers and IR
from Memory import ProcessorMemoryInterface# processor memory interface
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
#current = Current()	#how to use hazard table??	hazard_unit.curent

class ControlBooleans:
    def __init__(self):
        self.decode_stall=False
        self.fetch_stall=False
        self.execute_stall=False
        self.branch_prediction=False
        self.global_terminate=True
    
forward_bool=ControlBooleans()
    # Muxes
    # MuxAout=0 # input 1 of ALU
    # MuxBout=0 # input 2 of ALU
    # MuxYout=0 # output of MuxY
    
    # def MuxY(MuxY_select):
    #     global MuxYout
    #     if MuxY_select==0:
    #         MuxYout=buffer.getRZ()
    #     elif MuxY_select==1:
    #         MuxYout=memory.MDR
    #     elif MuxY_select==2:
    #         MuxYout=IAGmodule.PC_temp
    #     return MuxYout

###########Stage functions###############
def fetch(stage, clock):
        # to do here
        # if terminate==1, return
        # operation queue will be used in the buffer update stage, not here.
        # fetch the instruction using the value in PC
        # compare it to BTB to check if that is a branch/jump. If it is, update PC to the target.
        # remember to enqueue the PC into the decode_PC_queue
    control_module.controlStateUpdate(0)
    if(control_module.terminate):
        return
    # if not control_module.fetch_deque_signal():
    #     return
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

def decode(stage, clock):
        # if terminate==1, return
    if control_module.terminate:
        return
    if not (control_module.decode_deque_signal()):
        return
            #decode stalled
        # check the operation queue. If empty, then operate. Else, don't operate and pop.

        # decode the instruction first in the IR
    forward_bool.global_terminate=False
    control_module.decode(registers.ReadIR(),IAGmodule.PC)
    if control_module.terminate:
        return
        # check for hazards(in this case stalls) using the hazard table.
    data_hazard=hazard_module.decision_maker(control_module.opcode, control_module.funct3, control_module.rs1, control_module.rs2, control_module.rd, 0) 	#requires stall, forwarding kno is turned off, replace 0 with knob signal
            #write stalling code
    if data_hazard!=-1: # data hazard handled
        print(f"##########  DATA HAZARD code {data_hazard}   ##############")
        forward_bool.decode_stall = True
        forward_bool.fetch_stall=True
        control_module.execute_set_NOP()
        control_module.memory_set_NOP()
        control_module.register_set_NOP()
        return
        # follow steps given in documentation to resolve the hazard by stalling/data forwarding.
        # if all good, push the decoded the signals into the queues.
    MuxAout=0
    MuxBout=0
    # if buffer.R2bool==True:
    #     MuxBout=buffer.R2
    #     buffer.R2bool=False
    if control_module.MuxBSelect==0:
        MuxBout=registers.ReadGpRegisters(control_module.rs2)
    elif control_module.MuxBSelect==1:
        MuxBout=control_module.imm
    # if buffer.R1bool==True:
    #     MuxBout=buffer.R1
    #     buffer.R1bool=False
    if control_module.MuxASelect==0:
        MuxAout=registers.ReadGpRegisters(control_module.rs1)
    elif control_module.MuxASelect==1:
        MuxAout=buffer.Decode_input_PC
    # code for executing ALU for branch misprediction here.
    # if not control_module.jump:
    buffer.RAtemp=MuxAout
    buffer.RBtemp=MuxBout
    buffer.RMtemp=registers.ReadGpRegisters(control_module.rs2)
    control_module.RM_placeholder=buffer.RMtemp
    control_module.RA_placeholder=buffer.Decode_input_PC+4 # return address
    # if mtod or to_return:
    #     return
    ALUmodule.outputBool=0
    if control_module.branch:
        ALUmodule.ALUexecute(control_module.ALUOp, control_module.ALUcontrol, buffer.RAtemp, buffer.RBtemp)
    IAGmodule.PC_buffer=buffer.Decode_input_PC
    control_module.branching_controlUpdate(ALUmodule.outputBool)
    IAGmodule.PCset(buffer.RAtemp, control_module.MuxPCSelect)
    IAGmodule.SetBranchOffset(control_module.imm)
    IAGmodule.PCUpdate(control_module.MuxINCSelect) # value in PC_buffer
    print(f"\t\t\tiag pc buffer {hex(IAGmodule.PC_buffer)}")
    #buffer.Decode_output_PC_temp=IAGmodule.PC_buffer
    # use branch prediction from the buffer
    print(f"RAtemp-{buffer.RAtemp} RBtemp-{buffer.RBtemp} RA-{buffer.RA} RB-{buffer.RB}")
    print(f"\t\t\tRA placeholder- {control_module.RA_placeholder}")
    control_module.branch_misprediction=buffer.Decode_input_branch_prediction^(control_module.jump or (control_module.branch and ALUmodule.outputBool))

    if buffer.Decode_input_branch_prediction==0 and (control_module.jump or control_module.branch):
        print(f"BTB entry created. {IAGmodule.PC_buffer}")
        IAGmodule.BTB_insert(buffer.Decode_input_PC,IAGmodule.PC_buffer,1)
    # if control_module.branch and not ALU.outputBool:
    #     print("BTB entry created")
    #     IAGmodule.BTB_insert(buffer.Decode_input_PC,IAGmodule.PC_buffer,1)
    if control_module.branch_misprediction: 
        # code here for handling branch misprediction
        print("Misprediction")
        # if control_module.jump or control_module.branch:
        #     print("BTB entry created")
        #     IAGmodule.BTB_insert(buffer.Decode_input_PC,IAGmodule.PC_buffer,1)
        control_module.decode_operation.append(False) # -2 is the code to indicate a branch misprediction and the decode unit does not have to operate
        #buffer.Decode_output_PC_temp=buffer.Decode_input_PC+4 # set the accurate target PC
        # if control_module.jump:
        #     if control_module.
        # if control_module.branch:
            
        # else: # in this case, branch was T but the truth was NT
        #     buffer.Decode_output_PC_temp=buffer.Decode_input_PC+4
        #print(f"\t\t\tiag pc buffer{hex(IAGmodule.PC_buffer)}")
        hazard_module.add_inst(control_module.opcode, control_module.funct3, control_module.rs1, control_module.rs2, control_module.rd)
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
    hazard_module.add_inst(control_module.opcode, control_module.funct3, control_module.rs1, control_module.rs2, control_module.rd)
    control_module.execute_set_operate()
    control_module.memory_set_operate()
    control_module.register_set_operate()


# def execute(stage): # ALU

#         # dequeue from the control signals. Check if we need to operate or not
#     if not control_module.execute_deque_signal():
#         return
#             # return code
#     forward_bool.global_terminate=False
#     ALUmodule.ALUexecute(control_module.ALUOp, control_module.ALUcontrol,buffer.getRA, buffer.getRB)   # This will perform the required Arithmetic / logical operation
#         # this will put the value obtained from ALU after execution  in RZ buffer
#         #buffers.RZtemp=ALUmodule.output32
#     buffer.setRZtemp(ALUmodule.output32)
def execute(stage,clock): # ALU
    # dequeue from the control signals. Check if we need to operate or not
    #False == NOP, 
    if not control_module.execute_deque_signal(): # this function returns False if memory is in NOP. Also, all control_module.ALUop, etc are updated to 0 in case of NOP, or correct value if OP
        # perform other tasks and return
        return
    forward_bool.global_terminate=False
    print("Execute Stage")
    # can use control_module.ALUop etc directly to use as arguments to ALU.
    print(f"ALUcontrol-{control_module.ALUcontrol} ALUop-{control_module.ALUOp}")
    ALUmodule.ALUexecute(control_module.ALUOp, control_module.ALUcontrol,buffer.getRA(), buffer.getRB())
    buffer.RZtemp=ALUmodule.output32	#simple execution
    print(f"clock- {clock} RZtemp-{buffer.RZtemp} ALUoutput-{ALUmodule.output32}")
    #add this code at the end of cycle
    #if(EtoE){
      #buffer.set
    #}  

def mem_access(stage, clock):
        # dequeue from the control signals. Check if we need to operate or not
    if not control_module.memory_deque_signal():
            # return code
        return
    forward_bool.global_terminate=False
    memory.AccessMemory(control_module.MemRead, control_module.MemWrite, buffer.getRZ(), control_module.BytesToAccess, control_module.RM_placeholder) # why RMtemp? RM is updated at the end of cycle
    print(f"Memory MDR- {memory.MDR} Memory MAR- {memory.MAR}")
    # MuxY
    print(f"MuxYSelect {control_module.MuxYSelect}") 
    if control_module.MuxYSelect == 0:
        print("RZ to RY")
        buffer.RYtemp = buffer.getRZ()
    elif control_module.MuxYSelect == 1:
        print(f"MDR to RY {memory.MDR}")
        buffer.RYtemp = memory.MDR
    elif control_module.MuxYSelect == 2:
        print(f"\t\tRY set to RA!! {control_module.RA_placeholder}")
        buffer.RYtemp 
    # control_module.controlStateUpdate(stage)
    # memory.AccessMemory(control_module.MemRead,control_module.MemWrite,buffer.getRZtemp(),control_module.BytesToAccess,buffer.getRMtemp())
    
def reg_writeback(stage, clock):
# dequeue from the control signals. Check if we need to operate or not
    if not control_module.register_deque_signal(): # this function returns False if reg_write_back is in NOP. Also, all control_module.ALUop, etc are updated to 0 in case of NOP, or correct value if OP
        # perform other tasks and return
        return
    forward_bool.global_terminate=False
    print("RegisterWrite stage")
    registers.WriteGpRegisters(control_module.rd,control_module.RegWrite,buffer.getRY())  # This will simply write back to the registers based on the control signal

    # dequeue from the control signals. Check if we need to operate or not
def buffer_update():
    if not forward_bool.fetch_stall:
        # buffer.setR1(buffer.getR1temp)
        # buffer.setR2(buffer.getR2temp)
        registers.WriteIR(buffer.IRbuffer,1)
        buffer.Decode_input_branch_prediction=forward_bool.branch_prediction
        buffer.Decode_input_PC=IAGmodule.PC
        if not control_module.branch_misprediction:
            IAGmodule.PC=buffer.Fetch_output_PC_temp
    if not forward_bool.decode_stall:
        # buffer.setRA(buffer.RAtemp,1)
        # buffer.setRB(buffer.RBtemp,1)
        buffer.RA=buffer.RAtemp
        buffer.RB=buffer.RBtemp

        if control_module.branch_misprediction:
            # IAGmodule.PC=buffer.Decode_output_PC_temp
            IAGmodule.PC=IAGmodule.PC_buffer

    buffer.RZ=buffer.RZtemp
    buffer.RY=buffer.RYtemp

    if forward_bool.fetch_stall or forward_bool.decode_stall:
        hazard_module.add_null()

    forward_bool.fetch_stall = False

    #if not forward_bool.decode_stall:
    forward_bool.decode_stall = False

    print(f"RZ update, temp-{buffer.RZtemp}, RZ-{buffer.RZ}")
    print(f"buff update- RAtemp-{buffer.RAtemp} RBtemp-{buffer.RBtemp} RA-{buffer.RA} RB-{buffer.RB}")
    # def buffer_update():
    #     if not forward_bool.fetch_stall:
    #         #buffer.setR1(buffer.getR1temp)
    #         #buffer.setR2(buffer.getR2temp)
    #         buffer.Decode_input_branch_prediction=forward_bool.branch_prediction
    #         buffer.Decode_input_PC=IAGmodule.PC
    #         if not control_module.branch_misprediction:
    #             IAGmodule.PC=buffer.Fetch_output_PC_temp
    #         #fetch ke konse buffer hain?
    #     if not forward_bool.decode_stall:
    #         buffer.setRA(buffer.getRAtemp)
    #         buffer.setRB(buffer.getRBtemp)
    #         if control_module.branch_misprediction:
    #             IAGmodule.PC=buffer.Decode_output_PC_temp
    #         #decode ke konse buffer hain aur?
    #     #if not forward_bool.execute_stall:
    #         buffer.setRZ(buffer.getRZtemp)	#RZ update
    #         buffer.setRM(buffer.getRMtemp)
    #         buffer.setRY(buffer.getRYtemp)
    #         #RY temp toh nahi hai na kuchh?

    #     #if not forward_bool.fetch_stall:
    #     forward_bool.fetch_stall = False

    #     #if not forward_bool.decode_stall:
    #     forward_bool.decode_stall = False

    #     #if not forward_bool.execute_stall:
    #     #forward_bool.execute_stall = False

def RunSim():
    clock=1
    while(True):
            # run the stages here, preferably in reverse order.
            # update the buffers in the end
        print(f"Clock Cycle-{clock}")
        forward_bool.global_terminate=True
        reg_writeback(4, clock)
        mem_access(3,clock)
        execute(2,clock)
        decode(1,clock)
        fetch(0,clock)
        buffer_update()
        print(f"PC{(IAGmodule.PC)} IR {hex(registers.IR)} RZ {buffer.RZ} RY {buffer.RY}\n###########################################\n")
        print(f"Hazard table {hazard_module.print_table()}")
        clock=clock+1
        if forward_bool.global_terminate:
            print("\033[1;92m\nProgram Terminated Successfully\033[0m")
            return