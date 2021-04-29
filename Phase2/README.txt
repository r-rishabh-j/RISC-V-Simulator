CS204 AY 2020-21 Sem2 Project: RISC-V 32I Simulator
Language for Source Code: Python

TEAM DETAILS: Group 3
Ayush Verma 2019CSB1147
Bhumika 2019CSB1152
Keshav Krishna 2019CSB1224
Rishabh Jain 2019CSB1286
Vishawam Datta 2019CSB1305

HOW TO RUN:
Clone the repository to your local system. After ensuring the installation of the following dependencies, run the steps as mentioned hereafter.
Libraries and installation Requirements:
-Python >=3.3
-importlib
-numpy

Steps to run via command-line interface for pipelined and with data forwarding:
Enter your machine code in a file with an appropriate file name.
Run the command python main.py <path to instruction file> on windows or python3 main.py <path to instruction file> on mac or Linux.
User will be prompted to set knobs for the simulator. Inputs for setting the knobs would be printed on the commandline interface.
Meaningful messages from the simulator will be displayed on the terminal.
Register and memory outputs will be stored in RegisterDump_<knob_config>.mc and MemoryDump_<knob_config>.mc respectively. User will be informed at the end of the 
program where the output has been directed to.
 
PHASE2 DESCRIPTION:

A pipelined implementation that supports stalling, data forwarding, control hazard detection and static branch prediction of the 5-step-single-cycle instruction execution is done. The input is taken in the form of a list of machine codes in the format:
<address of instruction> <machine code of the instruction> <optional ‘#’ beginning comments>
Text segment has to be flagged by ‘~text’ and the data segment by ‘~data’.
The program terminates with the "<address of instruction> 0x11" code.
Type of instructions supported:
R format - add, and, or, sll, slt, sra, srl, sub, xor, mul, div, rem
I format - addi, andi, ori, lb,  lh, lw, jalr
S format - sb, sw, sh
SB format - beq, bne, bge, blt
U format - auipc, lui
UJ format - jal

The code runs the machine code by running all 5 stages of the execution process at the same time and stalls, forwards data whenever required. The code supports and successfully executes programs comprising the above instruction types and is tested on programs like Fibonacci, Factorial and Bubble Sort.
 
CONTRIBUTIONS:
As a team effort, no strict separation was followed. A loose outline of the work is as follows:
Ayush Verma: Hazard Unit(Check_dependence, type of forwarding and type of stalling), Decode unit functions, Register And Memory Update functions.
Bhumika: Decode unit, Control Circuitry including Control Signals and ALU Control, Buffers, Hazard Table, Data Forwarding
Keshav Krishna: Buffers, Program Flow(pipelining), Control Circuit, some parts of memory, GUI
Rishabh Jain: Memory, register, ALU, Control and program flow and GUI,stalling mechanism, forwarding mechanism, control signal queues, Branch predictor
Vishawam Datta: Hazard Unit(Check_dependence, type of forwarding and type of stalling), Program Flow, IAG module including BTB, memory module and some parts of Control 

