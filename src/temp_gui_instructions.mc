#.data
#size: .word 5
#array:
#.word 10
#.word 30
#.word 20
#.word 0
#.word 50
#address: .word 0x10000020
~data
0x10000000 0x5
0x10000004 0xA
0x10000008 0x1e
0x1000000C 0x14
0x10000010 0x0
0x10000014 0x32
0x10000018 0x10000020
~text
0x0	0x10000517	#auipc x10 65536	la x10, array
0x4	0x00450513	#addi x10 x10 4	la x10, array
0x8	0x10000597	#auipc x11 65536	lw x11, size
0xc	0xFF85A583	#lw x11 -8(x11)	lw x11, size
0x10	0x10000617	#auipc x12 65536	lw x12, address
0x14	0x00862603	#lw x12 8(x12)	lw x12, address
0x18	0x00000693	#addi x13 x0 0	addi x13, x0, 0 #counter i
0x1c	0x000508B3	#add x17 x10 x0	add x17,x10, x0
0x20	0x00060E33	#add x28 x12 x0	add x28, x12, x0
0x24	0x00B68E63	#beq x13 x11 28	beq x13, x11, exitcopy
0x28	0x0008A783	#lw x15 0(x17)	lw x15, 0(x17)
0x2c	0x00FE2023	#sw x15 0(x28)	sw x15, 0(x28)
0x30	0x00168693	#addi x13 x13 1	addi x13, x13, 1
0x34	0x00488893	#addi x17 x17 4	addi x17, x17, 4
0x38	0x004E0E13	#addi x28 x28 4	addi x28, x28, 4
0x3c	0xFE9FF06F	#jal x0 -24	j copy
0x40	0x008000EF	#jal x1 8	jal x1, bubble_sort
0x44	0x0600006F	#jal x0 96	j exit
0x48	0x00100293	#addi x5 x0 1	addi x5, x0, 1
0x4c	0x04558A63	#beq x11 x5 84	beq x11, x5, return #n==1
0x50	0xFFF58713	#addi x14 x11 -1	addi x14, x11, -1
0x54	0x00000693	#addi x13 x0 0	addi x13, x0, 0 #counter i
0x58	0x000608B3	#add x17 x12 x0	add x17,x12, x0
0x5c	0x02E68263	#beq x13 x14 36	beq x13, x14, exitloop
0x60	0x0008A783	#lw x15 0(x17)	lw x15, 0(x17)
0x64	0x0048A803	#lw x16 4(x17)	lw x16, 4(x17)
0x68	0x00F85663	#bge x16 x15 12	bge x16, x15, continue
0x6c	0x00F8A223	#sw x15 4(x17)	sw x15, 4(x17)
0x70	0x0108A023	#sw x16 0(x17)	sw x16, 0(x17)
0x74	0x00168693	#addi x13 x13 1	addi x13, x13, 1
0x78	0x00488893	#addi x17 x17 4	addi x17, x17, 4
0x7c	0xFE1FF06F	#jal x0 -32	j loop
0x80	0xFF810113	#addi x2 x2 -8	addi sp, sp, -8
0x84	0x00112223	#sw x1 4(x2)	sw x1, 4(sp)
0x88	0x00B12023	#sw x11 0(x2)	sw x11, 0(sp)
0x8c	0xFFF58593	#addi x11 x11 -1	addi x11, x11, -1
0x90	0xFB9FF0EF	#jal x1 -72	jal x1, bubble_sort
0x94	0x00012583	#lw x11 0(x2)	lw x11, 0(sp)
0x98	0x00412083	#lw x1 4(x2)	lw x1, 4(sp)
0x9c	0x00810113	#addi x2 x2 8	addi sp, sp, 8
0xa0	0x00008067	#jalr x0 x1 0	jalr x0, x1, 0
0xa4    0x11
