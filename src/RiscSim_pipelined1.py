#!/usr/bin/python3
# this file contains code for the simulator. Contains the ALU
from Registers import Registers as reg  # contains 32 GP registers and IR
from Memory import ProcessorMemoryInterface  # processor memory interface
from ControlCircuit import ControlModule  # generates control signals
from IAG import InstructionAddressGenerator
from ALU import ArithmeticLogicUnit
from Buffers import Buffers

MAX_SIGNED_NUM = 0x7fffffff
MIN_SIGNED_NUM = -0x80000000
MAX_UNSIGNED_NUM = 0xffffffff
MIN_UNSIGNED_NUM = 0x00000000
registers = reg()  # register object
memory = ProcessorMemoryInterface()
control_module0 = ControlModule()
control_module1 = ControlModule()
control_module2 = ControlModule()
control_module3 = ControlModule()
control_module4 = ControlModule()
ALUmodule = ArithmeticLogicUnit()
IAGmodule = InstructionAddressGenerator()
buffer0 = Buffers()
buffer1 = Buffers()
buffer2 = Buffers()
buffer3 = Buffers()
buffer4 = Buffers()

# Muxes
MuxAout = 0  # input 1 of ALU
MuxBout = 0  # input 2 of ALU
MuxYout = 0  # output of MuxY


def MuxB(MuxB_select):
    global MuxBout
    if MuxB_select == 0:
        MuxBout = registers.ReadGpRegisters(control_module.rs2)
    elif MuxB_select == 1:
        MuxBout = control_module.imm
    return MuxBout


def MuxA(MuxA_select):
    global MuxAout
    if MuxA_select == 0:
        MuxAout = registers.ReadGpRegisters(control_module.rs1)
    elif MuxA_select == 1:
        MuxAout = IAGmodule.PC
    return MuxAout


def MuxY(MuxY_select):
    global MuxYout
    if MuxY_select == 0:
        MuxYout = buffer.getRZ()
    elif MuxY_select == 1:
        MuxYout = memory.MDR
    elif MuxY_select == 2:
        MuxYout = IAGmodule.PC_temp
    return MuxYout


###########Stage functions###############
def fetch(stage, check):
    if check == 0:
        # control state update function to be called here
        control_module0.controlStateUpdate(stage)
        memory.LoadInstruction(IAGmodule.PC)  # this will fetch the instruction and put it in MDR
        registers.WriteIR(memory.MDR, control_module0.IRwrite)  # This loads the Instruction from MDR to IR
        IAGmodule.PCTempUpdate()  # this will do PC temp = PC + 4
    elif check == 1:
        # control state update function to be called here
        control_module1.controlStateUpdate(stage)
        memory.LoadInstruction(IAGmodule.PC)  # this will fetch the instruction and put it in MDR
        registers.WriteIR(memory.MDR, control_module1.IRwrite)  # This loads the Instruction from MDR to IR
        IAGmodule.PCTempUpdate()  # this will do PC temp = PC + 4
    elif check == 2:
        # control state update function to be called here
        control_module2.controlStateUpdate(stage)
        memory.LoadInstruction(IAGmodule.PC)  # this will fetch the instruction and put it in MDR
        registers.WriteIR(memory.MDR, control_module2.IRwrite)  # This loads the Instruction from MDR to IR
        IAGmodule.PCTempUpdate()  # this will do PC temp = PC + 4
    elif check == 3:
        # control state update function to be called here
        control_module3.controlStateUpdate(stage)
        memory.LoadInstruction(IAGmodule.PC)  # this will fetch the instruction and put it in MDR
        registers.WriteIR(memory.MDR, control_module3.IRwrite)  # This loads the Instruction from MDR to IR
        IAGmodule.PCTempUpdate()  # this will do PC temp = PC + 4
    elif check == 4:
        # control state update function to be called here
        control_module4.controlStateUpdate(stage)
        memory.LoadInstruction(IAGmodule.PC)  # this will fetch the instruction and put it in MDR
        registers.WriteIR(memory.MDR, control_module4.IRwrite)  # This loads the Instruction from MDR to IR
        IAGmodule.PCTempUpdate()  # this will do PC temp = PC + 4


def decode(stage, check):
    if check == 0:
        control_module0.controlStateUpdate(stage)
        global MuxAout
        global MuxBout
        control_module0.decode(registers.ReadIR(),
                              IAGmodule.PC)  # this will decode the instruction present in IR and then will set the controls based on the type of instructions
        # decode
        if (control_module0.terminate == 1):
            return

        buffer0.setRA(registers.ReadGpRegisters(
            control_module0.rs1))  # putting the value of RS1 in RA buffer which will then be sent to IAG as input wire
        buffer0.setRM(registers.ReadGpRegisters(control_module0.rs2))  # putting the value of RS2 in RM buffer
        IAGmodule.PCset(buffer0.getRA(),
                        control_module0.MuxPCSelect)  # this function will choose PC to be PC or RA based on the control signal generated
        IAGmodule.SetBranchOffset(control_module0.imm)  # this puts the immediate value decoded to the immediate wire in IAG

        # loading the register values
        MuxAout = MuxA(control_module0.MuxASelect)  # this will  (based on control)select what would go into 1st input of ALU
        MuxBout = MuxB(control_module0.MuxBSelect)  # this will (based on control) select what would go into 2nd input of ALU
    elif check == 1:
        control_module.controlStateUpdate(stage)
        global MuxAout
        global MuxBout
        control_module1.decode(registers.ReadIR(),
                              IAGmodule.PC)  # this will decode the instruction present in IR and then will set the controls based on the type of instructions
        # decode
        if (control_module1.terminate == 1):
            return

        buffer1.setRA(registers.ReadGpRegisters(
            control_module1.rs1))  # putting the value of RS1 in RA buffer which will then be sent to IAG as input wire
        buffer1.setRM(registers.ReadGpRegisters(control_module1.rs2))  # putting the value of RS2 in RM buffer
        IAGmodule.PCset(buffer1.getRA(),
                        control_module1.MuxPCSelect)  # this function will choose PC to be PC or RA based on the control signal generated
        IAGmodule.SetBranchOffset(
            control_module1.imm)  # this puts the immediate value decoded to the immediate wire in IAG

        # loading the register values
        MuxAout = MuxA(
            control_module1.MuxASelect)  # this will  (based on control)select what would go into 1st input of ALU
        MuxBout = MuxB(
            control_module1.MuxBSelect)  # this will (based on control) select what would go into 2nd input of ALU
    elif check == 2:
        control_module2.controlStateUpdate(stage)
        global MuxAout
        global MuxBout
        control_module2.decode(registers.ReadIR(),
                              IAGmodule.PC)  # this will decode the instruction present in IR and then will set the controls based on the type of instructions
        # decode
        if (control_module2.terminate == 1):
            return

        buffer2.setRA(registers.ReadGpRegisters(
            control_module2.rs1))  # putting the value of RS1 in RA buffer which will then be sent to IAG as input wire
        buffer2.setRM(registers.ReadGpRegisters(control_module2.rs2))  # putting the value of RS2 in RM buffer
        IAGmodule.PCset(buffer2.getRA(),
                        control_module2.MuxPCSelect)  # this function will choose PC to be PC or RA based on the control signal generated
        IAGmodule.SetBranchOffset(
            control_module2.imm)  # this puts the immediate value decoded to the immediate wire in IAG

        # loading the register values
        MuxAout = MuxA(
            control_module2.MuxASelect)  # this will  (based on control)select what would go into 1st input of ALU
        MuxBout = MuxB(
            control_module2.MuxBSelect)  # this will (based on control) select what would go into 2nd input of ALU
    elif check == 3:
        control_module3.controlStateUpdate(stage)
        global MuxAout
        global MuxBout
        control_module3.decode(registers.ReadIR(),
                              IAGmodule.PC)  # this will decode the instruction present in IR and then will set the controls based on the type of instructions
        # decode
        if (control_module3.terminate == 1):
            return

        buffer3.setRA(registers.ReadGpRegisters(
            control_module3.rs1))  # putting the value of RS1 in RA buffer which will then be sent to IAG as input wire
        buffer3.setRM(registers.ReadGpRegisters(control_module.rs2))  # putting the value of RS2 in RM buffer
        IAGmodule.PCset(buffer3.getRA(),
                        control_module3.MuxPCSelect)  # this function will choose PC to be PC or RA based on the control signal generated
        IAGmodule.SetBranchOffset(
            control_module3.imm)  # this puts the immediate value decoded to the immediate wire in IAG

        # loading the register values
        MuxAout = MuxA(
            control_module3.MuxASelect)  # this will  (based on control)select what would go into 1st input of ALU
        MuxBout = MuxB(
            control_module3.MuxBSelect)  # this will (based on control) select what would go into 2nd input of ALU
    elif check == 4:
        control_module4.controlStateUpdate(stage)
        global MuxAout
        global MuxBout
        control_module4.decode(registers.ReadIR(),
                              IAGmodule.PC)  # this will decode the instruction present in IR and then will set the controls based on the type of instructions
        # decode
        if (control_module4.terminate == 1):
            return

        buffer4.setRA(registers.ReadGpRegisters(
            control_module4.rs1))  # putting the value of RS1 in RA buffer which will then be sent to IAG as input wire
        buffer4.setRM(registers.ReadGpRegisters(control_module4.rs2))  # putting the value of RS2 in RM buffer
        IAGmodule.PCset(buffer4.getRA(),
                        control_module4.MuxPCSelect)  # this function will choose PC to be PC or RA based on the control signal generated
        IAGmodule.SetBranchOffset(
            control_module4.imm)  # this puts the immediate value decoded to the immediate wire in IAG

        # loading the register values
        MuxAout = MuxA(
            control_module4.MuxASelect)  # this will  (based on control)select what would go into 1st input of ALU
        MuxBout = MuxB(
            control_module4.MuxBSelect)  # this will (based on control) select what would go into 2nd input of ALU


def execute(stage, check):  # ALU
    if check == 0:
        control_module0.controlStateUpdate(stage)
        global MuxAout
        global MuxBout
        # print("ALUop is", control_module.ALUOp)
        # temp=control_module.ALUOp
        ALUmodule.ALUexecute(control_module0.ALUOp, control_module0.ALUcontrol, MuxAout,
                             MuxBout)  # This will perform the required Arithmetic / logical operation
        buffer0.setRZ(ALUmodule.output32)  # this will put the value obtained from ALU after execution  in RZ buffer

        control_module0.branching_controlUpdate(
            ALUmodule.outputBool)  # this will update MuxINCselect based on wether to jump or not based on the comparison
        IAGmodule.PCUpdate(
            control_module0.MuxINCSelect)  # this will update PC by adding immediate or by adding 4 based on the control signal provided
    elif check == 1:
        control_module1.controlStateUpdate(stage)
        global MuxAout
        global MuxBout
        # print("ALUop is", control_module.ALUOp)
        # temp=control_module.ALUOp
        ALUmodule.ALUexecute(control_module1.ALUOp, control_module1.ALUcontrol, MuxAout,
                             MuxBout)  # This will perform the required Arithmetic / logical operation
        buffer1.setRZ(ALUmodule.output32)  # this will put the value obtained from ALU after execution  in RZ buffer

        control_module1.branching_controlUpdate(
            ALUmodule.outputBool)  # this will update MuxINCselect based on wether to jump or not based on the comparison
        IAGmodule.PCUpdate(
            control_module1.MuxINCSelect)  # this will update PC by adding immediate or by adding 4 based on the control signal provided
    elif check == 2:
        control_module2.controlStateUpdate(stage)
        global MuxAout
        global MuxBout
        # print("ALUop is", control_module.ALUOp)
        # temp=control_module.ALUOp
        ALUmodule.ALUexecute(control_module2.ALUOp, control_module2.ALUcontrol, MuxAout,
                             MuxBout)  # This will perform the required Arithmetic / logical operation
        buffer2.setRZ(ALUmodule.output32)  # this will put the value obtained from ALU after execution  in RZ buffer

        control_module2.branching_controlUpdate(
            ALUmodule.outputBool)  # this will update MuxINCselect based on wether to jump or not based on the comparison
        IAGmodule.PCUpdate(
            control_module2.MuxINCSelect)  # this will update PC by adding immediate or by adding 4 based on the control signal provided
    elif check == 3:
        control_module3.controlStateUpdate(stage)
        global MuxAout
        global MuxBout
        # print("ALUop is", control_module.ALUOp)
        # temp=control_module.ALUOp
        ALUmodule.ALUexecute(control_module3.ALUOp, control_module3.ALUcontrol, MuxAout,
                             MuxBout)  # This will perform the required Arithmetic / logical operation
        buffer3.setRZ(ALUmodule.output32)  # this will put the value obtained from ALU after execution  in RZ buffer

        control_module3.branching_controlUpdate(
            ALUmodule.outputBool)  # this will update MuxINCselect based on wether to jump or not based on the comparison
        IAGmodule.PCUpdate(
            control_module3.MuxINCSelect)  # this will update PC by adding immediate or by adding 4 based on the control signal provided
    elif check == 4:
        control_module4.controlStateUpdate(stage)
        global MuxAout
        global MuxBout
        # print("ALUop is", control_module.ALUOp)
        # temp=control_module.ALUOp
        ALUmodule.ALUexecute(control_module4.ALUOp, control_module4.ALUcontrol, MuxAout,
                             MuxBout)  # This will perform the required Arithmetic / logical operation
        buffer4.setRZ(ALUmodule.output32)  # this will put the value obtained from ALU after execution  in RZ buffer

        control_module4.branching_controlUpdate(
            ALUmodule.outputBool)  # this will update MuxINCselect based on wether to jump or not based on the comparison
        IAGmodule.PCUpdate(
            control_module4.MuxINCSelect)  # this will update PC by adding immediate or by adding 4 based on the control signal provided


def mem_access(stage, check):
    if check == 0:
        control_module0.controlStateUpdate(stage)
        memory.AccessMemory(control_module0.MemRead, control_module0.MemWrite, buffer0.getRZ(), control_module0.BytesToAccess,
                            buffer0.getRM())  # Sent the value of RZ in MAR and sent the value of RM in MDR along with appropriate control signals , then based on this the data will be loaded or stored ,for loading data will be available in MDR
    elif check == 1:
        control_module1.controlStateUpdate(stage)
        memory.AccessMemory(control_module1.MemRead, control_module1.MemWrite, buffer1.getRZ(), control_module1.BytesToAccess,
                            buffer1.getRM())  # Sent the value of RZ in MAR and sent the value of RM in MDR along with appropriate control signals , then based on this the data wil
    elif check == 2:
        control_module2.controlStateUpdate(stage)
        memory.AccessMemory(control_module2.MemRead, control_module2.MemWrite, buffer2.getRZ(), control_module2.BytesToAccess,
                            buffer2.getRM())  # Sent the value of RZ in MAR and sent the value of RM in MDR along with appropriate control signals , then based on this the data wil
    elif check == 3:
        control_module3.controlStateUpdate(stage)
        memory.AccessMemory(control_module3.MemRead, control_module3.MemWrite, buffer3.getRZ(), control_module3.BytesToAccess,
                            buffer3.getRM())  # Sent the value of RZ in MAR and sent the value of RM in MDR along with appropriate control signals , then based on this the data wil
    elif check == 4:
        control_module4.controlStateUpdate(stage)
        memory.AccessMemory(control_module4.MemRead, control_module4.MemWrite, buffer4.getRZ(), control_module4.BytesToAccess,
                            buffer4.getRM())  # Sent the value of RZ in MAR and sent the value of RM in MDR along with appropriate control signals , then based on this the data wil

def reg_writeback(stage, check):
    if check == 0:
        control_module0.controlStateUpdate(stage)
        buffer0.setRY(MuxY(
            control_module0.MuxYSelect))  # sets the value of RY buffer as the output of MuxY which will be selected based on control signals
        registers.WriteGpRegisters(control_module0.rd, control_module0.RegWrite,
                                   buffer0.getRY())  # This will simply write back to the registers based on the control signal
    elif check == 1:
        control_module1.controlStateUpdate(stage)
        buffer1.setRY(MuxY(
            control_module1.MuxYSelect))  # sets the value of RY buffer as the output of MuxY which will be selected based on control signals
        registers.WriteGpRegisters(control_module1.rd, control_module1.RegWrite,
                                   buffer1.getRY())  # This will simply write back to the registers based on the control signal
    elif check == 2:
        control_module2.controlStateUpdate(stage)
        buffer2.setRY(MuxY(
            control_module2.MuxYSelect))  # sets the value of RY buffer as the output of MuxY which will be selected based on control signals
        registers.WriteGpRegisters(control_module2.rd, control_module2.RegWrite,
                                   buffer2.getRY())  # This will simply write back to the registers based on the control signal
    elif check == 3:
        control_module3.controlStateUpdate(stage)
        buffer3.setRY(MuxY(
            control_module3.MuxYSelect))  # sets the value of RY buffer as the output of MuxY which will be selected based on control signals
        registers.WriteGpRegisters(control_module3.rd, control_module3.RegWrite,
                                   buffer3.getRY())  # This will simply write back to the registers based on the control signal
    elif check == 4:
        control_module4.controlStateUpdate(stage)
        buffer4.setRY(MuxY(
            control_module4.MuxYSelect))  # sets the value of RY buffer as the output of MuxY which will be selected based on control signals
        registers.WriteGpRegisters(control_module4.rd, control_module4.RegWrite,
                                   buffer4.getRY())  # This will simply write back to the registers based on the control signal


def RunSim():
    # loop
    clock = 1
    while (1):
        print(f"\n\033[1;96mCycle {clock}\033[0m")
        stage = 0
        fetch(stage)
        stage = 1
        decode(stage)
        #if (control_module.terminate == 1):
        #    return
        stage = 2
        execute(stage)
        stage = 3
        mem_access(stage)
        stage = 4
        reg_writeback(stage)
        clock = clock + 1


def RunSim_pipelined():
    clock = 1
    check = (IAGmodule.PC/4)%5
    if check == 0:
        while (1):
            print(f"\n\033[1;96mCycle {clock}\033[0m")
            stage = 0
            fetch(stage, check)
            RunSim_pipelined()
            stage = 1
            decode(stage, check)
            if (control_module0.terminate == 1):
                return
            stage = 2
            execute(stage, check)
            stage = 3
            mem_access(stage, check)
            stage = 4
            reg_writeback(stage, check)
            clock = clock + 1
    elif check == 1:
        while (1):
            print(f"\n\033[1;96mCycle {clock}\033[0m")
            stage = 0
            fetch(stage, check)
            RunSim_pipelined()
            stage = 1
            decode(stage, check)
            if (control_module1.terminate == 1):
                return
            stage = 2
            execute(stage, check)
            stage = 3
            mem_access(stage, check)
            stage = 4
            reg_writeback(stage, check)
            clock = clock + 1
    elif check == 2:
        while (1):
            print(f"\n\033[1;96mCycle {clock}\033[0m")
            stage = 0
            fetch(stage, check)
            RunSim_pipelined()
            stage = 1
            decode(stage, check)
            if (control_module0.terminate == 1):
                return
            stage = 2
            execute(stage, check)
            stage = 3
            mem_access(stage, check)
            stage = 4
            reg_writeback(stage, check)
            clock = clock + 1
    elif check == 3:
        while (1):
            print(f"\n\033[1;96mCycle {clock}\033[0m")
            stage = 0
            fetch(stage, check)
            RunSim_pipelined()
            stage = 1
            decode(stage, check)
            if (control_module0.terminate == 1):
                return
            stage = 2
            execute(stage, check)
            stage = 3
            mem_access(stage, check)
            stage = 4
            reg_writeback(stage, check)
            clock = clock + 1
    elif check == 4:
        while (1):
            print(f"\n\033[1;96mCycle {clock}\033[0m")
            stage = 0
            fetch(stage, check)
            RunSim_pipelined()
            stage = 1
            decode(stage, check)
            if (control_module0.terminate == 1):
                return
            stage = 2
            execute(stage, check)
            stage = 3
            mem_access(stage, check)
            stage = 4
            reg_writeback(stage, check)
            clock = clock + 1
