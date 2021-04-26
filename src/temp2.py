#!/usr/bin/python3
# this file contains code for the simulator. Contains the ALU
from Registers import Registers as reg # contains 32 GP registers and IR
from Memory import ProcessorMemoryInterface# processor memory interface
from ControlCircuit import ControlModule # generates control signals
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

class ControlBooleans:
  	def __init__(self):
        self.decode_stall=False
        self.fetch_stall=False
        self.execute_stall=False
		self.branch_prediction=False

forward_bool=ControlBooleans()
# Muxes
MuxAout=0 # input 1 of ALU
MuxBout=0 # input 2 of ALU
MuxYout=0 # output of MuxY
def MuxB(MuxB_select):
    global MuxBout
    if MuxB_select==0:
        MuxBout=registers.ReadGpRegisters(control_module.rs2)
    elif MuxB_select==1:
        MuxBout=control_module.imm
    return MuxBout
def MuxA(MuxA_select):
    global MuxAout
    if MuxA_select==0:
        MuxAout=registers.ReadGpRegisters(control_module.rs1)
    elif MuxA_select==1:
        MuxAout=IAGmodule.PC
    return MuxAout
def MuxY(MuxY_select):
    global MuxYout
    if MuxY_select==0:
        MuxYout=buffer.getRZ()
    elif MuxY_select==1:
        MuxYout=memory.MDR
    elif MuxY_select==2:
        MuxYout=IAGmodule.PC_temp
    return MuxYout

###########Stage functions###############
def fetch(stage):
    # to do here
    # if terminate==1, return
    # operation queue will be used in the buffer update stage, not here.
    # fetch the instruction using the value in PC
    # compare it to BTB to check if that is a branch/jump. If it is, update PC to the target.
    # remember to enqueue the PC into the decode_PC_queue

def decode(stage):
    # if terminate==1, return
    # check the operation queue. If empty, then operate. Else, don't operate and pop.
    # decode the instruction first in the IR
    # check for hazards using the hazard table.
    # follow steps given in documentation to resolve the hazard by stalling/data forwarding.
    # if all good, push the decoded the signals into the queues.

def execute(stage): # ALU
    # dequeue from the control signals. Check if we need to operate or not
    if not control_module.execute_deque_signal():
      	# return code
    ALUmodule.ALUexecute(control_module.ALUOp, control_module.ALUcontrol,MuxAout, MuxBout)   # This will perform the required Arithmetic / logical operation
     # this will put the value obtained from ALU after execution  in RZ buffer
    buffers.RZtemp=ALUmodule.output32
	
def mem_access(stage):
    # dequeue from the control signals. Check if we need to operate or not
	if not control_module.memory_deque_signal():
      	# return code
    control_module.controlStateUpdate(stage)
    memory.AccessMemory(control_module.MemRead,control_module.MemWrite,buffer.getRZtemp(),control_module.BytesToAccess,buffer.getRMtemp())
def reg_writeback(stage):
  
  	if not control_module.register_deque_signal():
      	# return code
  	buffer.RYtemp=MuxY(control_module.MuxYSelect)    # sets the value of RY buffer as the output of MuxY which will be selected based on control signals
    registers.WriteGpRegisters(control_module.rd,control_module.RegWrite,buffer.getRYtemp())  # This will simply write back to the registers based on the control signal

    # dequeue from the control signals. Check if we need to operate or not

def buffer_update():

def RunSim():
    clock=1
    while(True):
        # run the stages here, preferably in reverse order.
        # update the buffers in the end