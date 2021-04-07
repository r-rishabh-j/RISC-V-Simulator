# RISC-V-SIMULATOR

CS204 AY 2020-21 Sem2 Project: RISC-V 32I Simulator

Language for Source Code: Python

GUI : PyQt5

**TEAM DETAILS:**

&nbsp;&nbsp;&nbsp;&nbsp;Ayush Verma		2019CSB1147
&nbsp;&nbsp;&nbsp;&nbsp;Bhumika			2019CSB1152
&nbsp;&nbsp;&nbsp;&nbsp;Keshav Krishna	2019CSB1224
&nbsp;&nbsp;&nbsp;&nbsp;Rishabh Jain	2019CSB1286
&nbsp;&nbsp;&nbsp;&nbsp;Vishawam Datta	2019CSB1305

**HOW TO RUN:**
    Clone the repository to your local system. After ensuring the installation of the following dependencies, run the steps as mentioned hereafter.

    Libraries and installation Requirements:
	-Python >=3.3
	-importlib
	-numpy
	-PyQt5 >= 5.12
    
**Steps to run via GUI:**
	-Run the command “python gui6.py” or “python3 gui6,py” on Windows and Linux 		 respectively(name to be decided later)
	-The user-interface pops up. Type in your machine code in the “Machine Code” Editor in the format specified in the description below.
	-Press the Run button. The Register and Memory state of the program is updated and displayed
	-Meaningful messages from the simulator will be displayed on the terminal.

**Steps to run via command line interface:**

	-Enter your machine code in instructions.mc(filename and case important)

	-Run the command ‘python main.py’ in windows and ‘python3 main.py’ in mac or linux.

	-Meaningful messages from the simulator will be displayed on the terminal.

	-Register and memory outputs will be stored in RegisterDump.mc and MemoryDump.mc respectively.

**PHASE1 DESCRIPTION:**
    A 5-step single-cycle instruction execution is implemented. The input is taken in the form of a list of machine codes in the format:
> <address of instruction> <machine code of the instruction> <optional ‘#’ beginning comments>
The program terminates with the <address of instruction> 0x11 code.

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

Information regarding the status of the program and the results including register values and memory elements are displayed with the help of a user-friendly GUI developed with PyQt(a sample shown below).


CONTRIBUTIONS:
As a team effort, no strict separation was followed. A loose outline of the work is as follows:
	-Ayush Verma:  Decode unit functions, Register And Memory Update functions. 
	-Bhumika: Decode unit, Control Circuitry including Control Signals and ALU Control, Buffers
	-Keshav Krishna: Control circuitry, memory, GUI frontend and backend
	-Rishabh Jain: Memory, register, ALU, some parts of Control, GUI
	-Vishawam Datta: Program Flow(RiscSim.py), IAG module , memory module and some parts of Control

