~data
0x10000000 0xA
0x10000004 0x28
0x10000008 0xf
0x1000000C 0x1e
0x10000010 0x50
0x10000014 0x28
0x10000018 0x2B
0x1000001C 0x5D
0x10000020 0x46
0x10000024 0x41
0x10000028 0x41
0x1000002C 0x31
0x10000030 0x28
0x10000034 0x21
0x10000038 0x4B
0x1000003C 0x5A
0x10000040 0x50
0x10000044 0x46
0x10000048 0x46
0x1000004C 0x50
0x10000050 0x5f
0x10000054 0x5f
~text
0x0	0x008000EF	#jal x1 8	jal x1, gradesheet
0x4	0x09C0006F	#jal x0 156	j EXIT
0x8	0x10000417	#auipc x8 65536	la x8,quiz
0xc	0x01440413	#addi x8 x8 20	la x8,quiz
0x10	0x01C00493	#addi x9 x0 28	li,x9,28
0x14	0xFFC10113	#addi x2 x2 -4	addi sp,sp,-4
0x18	0x00112023	#sw x1 0(x2)	sw x1,0(sp)
0x1c	0x010000EF	#jal x1 16	jal x1,bubble_sort
0x20	0x00012083	#lw x1 0(x2)	lw x1,0(sp)
0x24	0x00410113	#addi x2 x2 4	addi sp,sp,4
0x28	0x00008067	#jalr x0 x1 0	jalr x0,x1,0
0x2c	0xFFC48493	#addi x9 x9 -4	addi x9, x9, -4
0x30	0x00000293	#addi x5 x0 0	addi x5, x0, 0 # to be used in end condition for outer loop
0x34	0x06548463	#beq x9 x5 104	bs_loop1: beq x9, x5, bs_loop1_end
0x38	0xFFC10113	#addi x2 x2 -4	addi sp, sp, -4 #storing x5 on stack for use inside the loop
0x3c	0x00512023	#sw x5 0(x2)	sw x5, 0(sp)
0x40	0x00000313	#addi x6 x0 0	li x6, 0 # end condition for inner loop if x6==x9
0x44	0x04935463	#bge x6 x9 72	bs_loop2: bge x6, x9, bs_loop2_end
0x48	0xFFC10113  #	ddi x2 x2 -4	addi sp, sp, -4
0x4c	0x00612023	#sw x6 0(x2)	sw x6, 0(sp)
0x50	0x00830333	#add x6 x6 x8	add x6,x6,x8 #x6 now contains the address of the primary variable
0x54	0x00430393	#addi x7 x6 4	addi x7,x6,4
0x58	0x0003A283	#lw x5 0(x7)	lw x5,0(x7)
0x5c	0xFFC10113	#addi x2 x2 -4	addi sp,sp,-4
0x60	0x00912023	#sw x9 0(x2)	sw x9,0(sp) #using x9 for loading primary value thus saving on stack
0x64	0x00032483	#lw x9 0(x6)	lw x9,0(x6)
0x68	0x0092D663	#bge x5 x9 12	bge x5,x9,endif #swap x5 and x9 to reverse sort
0x6c	0x00532023	#sw x5 0(x6)	sw x5,0(x6) #swapping the values
0x70	0x0093A023	#sw x9 0(x7)	sw x9,0(x7)
0x74	0x00012483	#lw x9 0(x2)	lw x9,0(sp)
0x78	0x00410113	#addi x2 x2 4	addi sp,sp,4
0x7c	0x00012303	#lw x6 0(x2)	lw x6, 0(sp)
0x80	0x00410113	#addi x2 x2 4	addi sp, sp, 4
0x84	0x00430313	#addi x6 x6 4	addi x6, x6, 4
0x88	0xFBDFF06F	#jal x0 -68	j bs_loop2
0x8c	0x00012283	#lw x5 0(x2)	lw x5, 0(sp)
0x90	0x00410113	#addi x2 x2 4	addi sp, sp, 4
0x94	0xFFC48493	#addi x9 x9 -4	addi x9, x9, -4
0x98	0xF9DFF06F	#jal x0 -100	j bs_loop1
0x9c	0x00008067	#jalr x0 x1 0	jalr x0, x1, 0
0xA0    0x11