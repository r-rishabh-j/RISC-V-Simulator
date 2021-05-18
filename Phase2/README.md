# RISC-V-SIMULATOR

CS204 AY 2020-21 Sem2 Project: RISC-V 32I Simulator<br/>
Language for Source Code: Python</br>

**TEAM DETAILS: Group 3**<br/>
Ayush Verma		2019CSB1147<br/>
Bhumika			2019CSB1152<br/>
Keshav Krishna	2019CSB1224<br/>
Rishabh Jain	2019CSB1286<br/>
Vishawam Datta	2019CSB1305<br/>

**HOW TO RUN:**<br/>
    Clone the repository to your local system. After ensuring the installation of the following dependencies, run the steps as mentioned hereafter.

    Libraries and installation Requirements:
	-Python >=3.3
	-importlib
	-numpy

**Steps to run via command line interface:**
- Enter your machine code in a file with an appropriate file name.
- Run the command ```python main.py <path to instruction file>``` on windows or ```python3 main.py <path to instruction file>``` on mac or linux.
- User will be prompted to set knobs for the simulator. Inputs for setting the knobs would be printed on the commandline interface.
- Meaningful messages from the simulator will be displayed on the terminal.
- Register and memory outputs will be stored in RegisterDump_<knob_config>.mc and MemoryDump_<knob_config>.mc respectively. User will be informed at the end of the 
program where the output has been directed to.

**PHASE2 DESCRIPTION:**</br>
   A pipelined implementation that supports stalling, data forwarding, control hazard detection and static branch prediction of the 5-step-single-cycle instruction execution is done. The input is taken in the form of a list of machine codes in the format:

> \<address of instruction\> \<machine code of the instruction\> \<optional ‘#’ beginning comments\>

Text segment has to be flagged by ‘~text’ and the data segment by ‘~data’.
The program terminates with the "\<address of instruction> 0x11" code.

```
Type of instructions supported:
R format - add, and, or, sll, slt, sra, srl, sub, xor, mul, div, rem
I format - addi, andi, ori, lb,  lh, lw, jalr
S format - sb, sw, sh
SB format - beq, bne, bge, blt
U format - auipc, lui
UJ format - jal
```

The instruction goes through- fetch, decode, execute, memory access and write-back stage. This process is governed by a datapath and a control path depending on the type of the identified instruction and the corresponding fields. The code supports and successfully executes programs comprising the above instruction types and is tested on programs like Fibonacci, Factorial and Bubble Sort.


**CONTRIBUTIONS:**</br>
As a team effort, no strict separation was followed. A loose outline of the work is as follows:
- Ayush Verma:  Decode unit functions, Register And Memory dump functions. 
- Bhumika: Decode unit, Control Circuitry including Control Signals and ALU Control, Buffers
- Keshav Krishna: Control circuitry, memory, GUI frontend and backend
- Rishabh Jain: Memory, register, ALU, some parts of Control, program flow and GUI
- Vishawam Datta: Program Flow, IAG module , memory module and some parts of Control

