#!/usr/bin/python3
# this file contains code for the simulator. Contains the ALU
from Registers import Registers as reg # contains 32 GP registers and PC,IR
from Memory import ProcessorMemoryInterface# processor memory interface
from ControlCircuit import ControlModule # generates control signals
from IAG import InstructionAddressGenerator
from ALU import ArithmeticLogicUnit
from Buffers import Buffers

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
def fetch():

    IAGmodule.PcTempUpdate()  # this will do PC temp = PC + 4
    memory.LoadInstruction(IAGmodule.PC)  # this will fetch the instruction and put it in MDR
    registers.WriteIR(memory.MDR,control_module.IRwrite)  # This loads the Instruction from MDR to IR

def decode():
    global MuxAout
    global MuxBout
    control_module.decode(registers.ReadIR(True))  # this will decode the instruction present in IR and then will set the controls based on the type of instructions
    #decode
    buffer.setRA(registers.ReadGpRegisters(control_module.rs1))  # putting the value of RS1 in RA buffer which will then be sent to IAG as input wire

    IAGmodule.Pcset(buffer.getRA(),control_module.MuxPCSelect) # this function will choose PC to be PC or RA based on the control signal generated
    IAGmodule.SetBranchOffset(control_module.imm)  # this puts the immediate value decoded to the immediate wire in IAG

    #loading the register values
    MuxAout=MuxA(control_module.MuxAselect)   # this will  (based on control)select what would go into 1st input of ALU
    MuxBout=MuxB(control_module.MuxBselect)     # this will (based on control) select what would go into 2nd input of ALU

    buffer.setRM(registers.ReadGpRegisters(control_module.rs2))  # putting the value of RS2 in RM buffer

def execute(): # ALU

    global MuxAout
    global MuxBout

    ALUmodule.ALUexecute(control_module.ALUop, control_module.ALUcontrol,MuxAout, MuxBout)   # This will perform the required Arithmetic / logical operation
    control_module.branching_controlUpdate(ALUmodule.outputBool)  # this will update MuxINCselect based on wether to jump or not based on the comparison

    IAGmodule.PcUpdate(control_module.MuxINCSelect)  # this will update PC by adding immediate or by adding 4 based on the control signal provided

    buffer.setRZ(ALUmodule.output32)  # this will put the value obtained from ALU after execution  in RZ buffer

def mem_access():

    # ye thik krio , control_module.BytesToAccess define karo instead of 4 different variables.
    memory.AccessMemory(control_module.MemRead,control_module.MemWrite,buffer.getRZ(),control_module.BytesToAccess,buffer.getRM())  #Sent the value of RZ in MAR and sent the value of RM in MDR along with appropriate control signals , then based on this the data will be loaded or stored ,for loading data will be available in MDR

def reg_writeback():
    buffer.setRY(MuxY(control_module.MuxYSelect))    # sets the value of RY buffer as the output of MuxY which will be selected based on control signals
    registers.WriteGpRegisters(control_module.rd,control_module.RegWrite,buffer.getRY())  # This will simply write back to the registers based on the control signal


def RunSim():
    #loop
    fetch()
    decode()
    execute()
    mem_access()
    reg_writeback()
