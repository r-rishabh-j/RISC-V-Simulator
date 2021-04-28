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
hazard_unit=HazardUnit()
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
def fetch(stage):
        # to do here
        # if terminate==1, return
        # operation queue will be used in the buffer update stage, not here.
        # fetch the instruction using the value in PC
        # compare it to BTB to check if that is a branch/jump. If it is, update PC to the target.
        # remember to enqueue the PC into the decode_PC_queue
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

def decode(stage):
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
        # check for hazards(in this case stalls) using the hazard table.
    data_hazard=hazard_unit.decision_maker(control_module.opcode, control_module.funct3, control_module.rs1, control_module.rs2, control_module.rd, 0) 	#requires stall, forwarding kno is turned off, replace 0 with knob signal
            #write stalling code
    if data_hazard!=-1: # data hazard handled
        forward_bool.decode_stall = True
        forward_bool.fetch_stall=True
        control_module.execute_set_NOP()
        control_module.memory_set_NOP()
        control_module.register_set_NOP()
        return
        # follow steps given in documentation to resolve the hazard by stalling/data forwarding.
        # if all good, push the decoded the signals into the queues.
    ALUmodule.ALUexecute(control_module.ALUOp, control_module.ALUcontrol, buffer.RA, buffer.RB)	#comparator for branch
    control_module.branching_controlUpdate(ALUmodule.outputBool)
    IAGmodule.PCset(buffer.RA, control_module.MuxPCSelect)
    IAGmodule.SetBranchOffset(control_module.imm)
    IAGmodule.PCUpdate(control_module.MuxINCSelect)

        if control_module.branch_misprediction:
            # code here for handling branch misprediction
            control_module.decode_operation.append(-2) # -2 is the code to indicate a branch misprediction and the decode unit does not have to operate
            #buffer.Decode_output_PC_temp=buffer.Decode_input_PC+4 # set the accurate target PC
            # if control_module.jump:
            #     if control_module.
            # if control_module.branch:

            # else: # in this case, branch was T but the truth was NT
            #     buffer.Decode_output_PC_temp=buffer.Decode_input_PC+4
            buffer.Decode_output_PC_temp=IAGmodule.PC_buffer
            control_module.execute_set_operate()
            control_module.memory_set_operate()
            control_module.register_set_operate()
            control_module.execute_set_NOP()
            control_module.memory_set_NOP()
            control_module.register_set_NOP()
            return
            
        control_module.execute_set_operate()
        control_module.memory_set_operate()
        control_module.register_set_operate()

    def execute(stage): # ALU
        # dequeue from the control signals. Check if we need to operate or not
        if not control_module.execute_deque_signal():
            # return code
        forward_bool.global_terminate=False
        ALUmodule.ALUexecute(control_module.ALUOp, control_module.ALUcontrol,buffer.getRA, buffer.getRB)   # This will perform the required Arithmetic / logical operation
        # this will put the value obtained from ALU after execution  in RZ buffer
        #buffers.RZtemp=ALUmodule.output32
        buffer.setRZtemp(ALUmodule.output32)

    def mem_access(stage):
        # dequeue from the control signals. Check if we need to operate or not
        if not control_module.memory_deque_signal():
            # return code

        forward_bool.global_terminate=False
        
        control_module.controlStateUpdate(stage)
        memory.AccessMemory(control_module.MemRead,control_module.MemWrite,buffer.getRZtemp(),control_module.BytesToAccess,buffer.getRMtemp())
    def reg_writeback(stage):

        if not control_module.register_deque_signal():
            # return code
        forward_bool.global_terminate=False
        buffer.RYtemp=MuxY(control_module.MuxYSelect)    # sets the value of RY buffer as the output of MuxY which will be selected based on control signals
        registers.WriteGpRegisters(control_module.rd,control_module.RegWrite,buffer.getRYtemp())  # This will simply write back to the registers based on the control signal

    # dequeue from the control signals. Check if we need to operate or not

    def buffer_update():
        if not forward_bool.fetch_stall:
            #buffer.setR1(buffer.getR1temp)
            #buffer.setR2(buffer.getR2temp)
            buffer.Decode_input_branch_prediction=forward_bool.branch_prediction
            buffer.Decode_input_PC=IAGmodule.PC
            if not control_module.branch_misprediction:
                IAGmodule.PC=buffer.Fetch_output_PC_temp
            #fetch ke konse buffer hain?
        if not forward_bool.decode_stall:
            buffer.setRA(buffer.getRAtemp)
            buffer.setRB(buffer.getRBtemp)
            if control_module.branch_misprediction:
                IAGmodule.PC=buffer.Decode_output_PC_temp
            #decode ke konse buffer hain aur?
        #if not forward_bool.execute_stall:
            buffer.setRZ(buffer.getRZtemp)	#RZ update
            buffer.setRM(buffer.getRMtemp)
            buffer.setRY(buffer.getRYtemp)
            #RY temp toh nahi hai na kuchh?

        #if not forward_bool.fetch_stall:
        forward_bool.fetch_stall = False

        #if not forward_bool.decode_stall:
        forward_bool.decode_stall = False

        #if not forward_bool.execute_stall:
        #forward_bool.execute_stall = False

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
        clock=clock+1
        if forward_bool.global_terminate:
            return
