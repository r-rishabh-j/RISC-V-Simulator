# RISC-V-SIMULATOR

CS204 AY 2020-21 Sem2 Project: RISC-V 32I Simulator<br/>
Language for Source Code: Python</br>
GUI : PyQt5</br>

**TEAM DETAILS: Group 3**<br/>
Ayush Verma		2019CSB1147<br/>
Bhumika			2019CSB1152<br/>
Keshav Krishna	2019CSB1224<br/>
Rishabh Jain	2019CSB1286<br/>
Vishawam Datta	2019CSB1305<br/>

<p align="center">
<img src="https://github.com/r-rishabh-j/RISC-V-Simulator/blob/main/sample_gui.png" width="600" height="450">
</p>

**HOW TO RUN:**<br/>
    Clone the repository to your local system. After ensuring the installation of the following dependencies, run the steps as mentioned hereafter.

    Libraries and installation Requirements:
	-Python >=3.3
	-importlib
	-numpy
	-PyQt5 >= 5.12
    
**Steps to run via GUI:**
- Navigate to src/GUI
- Run the command ```python GuiSim.py``` or ```python3 GuiSim.py``` on Windows and Linux 		 respectively
- The user-interface pops up. Type in your machine code in the “Machine Code” Editor in the format specified in the description below.
- Press the assemble button to load the the program to memory
- Feed in the I$ and D$ specifications in bytes. Enter associativity as the number of blocks per set.
- Select one of the three pipelining configurations.
- Press the run button to execute the program or step button to step through the program.
- Meaningful messages from the simulator will be displayed on the terminal.
- Register, main memory and cache contents will be displayed on the interface.
- Cache stats contents and stats will be printed on the 'Cache' tab
- Register and memory outputs of the program will be saved in RegisterDump.mc and MemoryDump.mc respectively.

**Steps to run via command line interface:**
- Navigate to src/command_line
- Enter your machine code in a file with an appropriate file name.
- Run the command ```python main.py <path to instruction file>``` on windows or ```python3 main.py <path to instruction file>``` on mac or linux.
- User will be prompted to set knobs for pipelining configurations and cache specifications.
- Feed in the I$ and D$ specifications in bytes. Enter associativity as the number of blocks per set.
- Meaningful messages from the simulator will be displayed on the terminal.
- Register and memory outputs will be stored in RegisterDump_\<knob_config>.mc and MemoryDump_\<knob_config>.mc respectively. User will be informed the location of output at program termination.

**DESCRIPTION:**</br>

The simulator supports 5-stage-single-cycle pipelined execution, which includes control hazard detection, and their resolution via stalling/flushing and data forwarding.
A 1-bit static branch predictor for the 5-step-single-cycle instruction execution has been implemented.

A memory Hierarchy has been implemented with L1 cache and the main memory. The L1 cache
is set associative. Write through and write allocate policies have been followed. LRU block
eviction has been followed in the cache module.

Cache size, block size in bytes must be a power of 2 and at least 4 bytes. Cache associativity
must also be a power of 2, including 1.

Program input code:
The input is taken in the form of a list of machine codes in the format:
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

Information regarding the status of the program and the results including register values and memory elements are displayed with the help of a user-friendly GUI developed with PyQt5.

**CONTRIBUTIONS:**</br>
As a team effort, no strict separation was followed. A loose outline of the work is as follows:

- Ayush Verma: LRU Unit(Cache), Hazard Unit(Check_dependence, type of forwarding and type
of stalling), Decode unit functions, Register And Memory output functions.

- Bhumika: Decode unit, Control Circuitry including Control Signals and ALU Control, Buffers,
Hazard Table, Data Forwarding, GUI, some part of cache

- Keshav Krishna: Buffers, Program Flow(pipelining), Control Circuit, some parts of memory, some part of cache, GUI

- Rishabh Jain: Memory, register, ALU, Control and program flow and GUI(final), stalling
mechanism, forwarding mechanism, control signal queues, Branch prediction, cache read/write
methods and design

- Vishawam Datta: Hazard Unit(Check_dependence, type of forwarding and type
of stalling),LRU Unit (cache), IAG module including BTB, Program flow (Phase 1) , memory module and some parts of
Control

