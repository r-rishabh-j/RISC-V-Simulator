# ~data
# 0x10000000 0x3
~text
# #0x0	0x00C000EF	#jal x1 12	jal x1,l1
# #0x4	0x00500213	#addi x4 x0 5	l2:addi x4,x0,5
# #0x8	0x008003EF	#jal x7 8	jal x7,exit
# #0xc	0x000082E7	#jalr x5 x1 0	jalr x5,x1,0
# #0x10	0x00000033	#add x0 x0 x0	exit:add x0,x0,x0
# #0x14 0x11
# #0x0	0x10000537	#lui x10 65536	lui x10,0x10000
# #0x4	0x00500193	#addi x3 x0 5	addi x3,x0,5
# #0x8	0x00352023	#sw x3 0(x10)	sw x3,0(x10)
# # #0xc 0x11
# # 0x0	0x10000537	#lui x10 65536	lui x10,0x10000
# # 0x4	0x00A52023	#sw x10 0(x10)	sw x10,0(x10)
# # 0x8 0x11
# # 0x0	0x10000537	#lui x10 65536	lui x10,0x10000
# # 0x4	0x00052183	#lw x3 0(x10)	lw x3,0(x10)
# # 0x8	0x00352223	#sw x3 4(x10)	sw x3,4(x10)
# # 0xC 0x11
# 0x0	0xFFB00293
# 0x4 0x11
# 0x0	0x05C0006F	#jal x0 92	j main
# 0x4	0xFF810113	#addi x2 x2 -8	addi sp sp -8
# 0x8	0x00000033	#add x0 x0 x0	add x0,x0,x0
# 0xc	0x00000033	#add x0 x0 x0	add x0,x0,x0
# 0x10	0x00112023	#sw x1 0(x2)	sw x1 0(sp)
# 0x14	0x00A12223	#sw x10 4(x2)	sw x10 4(sp) ## we have loaded n = x10 in stack because it is bound to change in a recursive call
# 0x18	0x00100A93	#addi x21 x0 1	li x21 1
# 0x1c	0x00AA9863	#bne x21 x10 16	bne x21 x10 l1 ## if n=1
# 0x20	0x00100513	#addi x10 x0 1	li x10 1
# 0x24	0x00810113	#addi x2 x2 8	addi sp sp 8 ## freeing the stack space
# 0x28	0x00008F67	#jalr x30 x1 0	jalr x30 x1 0
# 0x2c	0x00412303	#lw x6 4(x2)	lw x6 4(sp) ## loading n in x6
# 0x30	0xFFF30513	#addi x10 x6 -1	addi x10 x6 -1
# 0x34	0xFD1FF0EF	#jal x1 -48	jal x1 fac
# 0x38	0x00000033	#add x0 x0 x0	add x0,x0,x0
# 0x3c	0x00000033	#add x0 x0 x0	add x0,x0,x0
# 0x40	0x00412303	#lw x6 4(x2)	lw x6 4(sp) ## loading n in x6 because x10 now has the value (n-1)!
# 0x44	0x02650533	#mul x10 x10 x6	mul x10 x10 x6
# 0x48	0x00012083	#lw x1 0(x2)	lw x1 0(sp) ## loading x1 becuase this was most certainly changed by several function calls ...
# 0x4c	0x00000033	#add x0 x0 x0	add x0,x0,x0
# 0x50	0x00000033	#add x0 x0 x0	add x0,x0,x0
# 0x54	0x00810113	#addi x2 x2 8	addi sp sp 8 ## now freeing up the stack and updating stack pointer
# 0x58	0x00008F67	#jalr x30 x1 0	jalr x30 x1 0
# 0x5c	0x10000517	#auipc x10 65536	lw x10 var1
# 0x60	0xFA452503	#lw x10 -92(x10)	lw x10 var1
# 0x64	0xFA1FF0EF	#jal x1 -96	jal x1 fac
# 0x0	0xFFC10113
# 0x4 0x11
# 0x0	0x03200513	#addi x10 x0 50	addi x10,x0,50
# 0x4	0xFF810113	#addi x2 x2 -8	addi sp,sp,-8
# 0x8	0x00A12023	#sw x10 0(x2)	sw x10,0(sp)
# 0xc	0x00A12223	#sw x10 4(x2)	sw x10,4(sp)
# # 0x10	0x00012583	#lw x11 0(x2)	lw x11,0(sp)
# # 0x14	0x00412603	#lw x12 4(x2)	lw x12,4(sp)
# # 0x18 0x11
# 0x0	0x00A00513	#addi x10 x0 10	addi x10,x0,10
# 0x4	0x00A28663	#beq x5 x10 12	loop: beq x5,x10,exit
# 0x8	0x00128293	#addi x5 x5 1	addi x5,x5,1
# 0xc	0xFF9FF0EF	#jal x1 -8	jal x1, loop
# 0x10 0x11
# 0x0	0x00A00513	#addi x10 x0 10	addi x10,x0,10
# 0x4	0x00A28A63	#beq x5 x10 20	loop: beq x5,x10,exit
# 0x8	0xFFC10113	#addi x2 x2 -4	addi sp,sp,-4
# 0xc	0x00512023	#sw x5 0(x2)	sw x5,0(sp)
# 0x10	0x00128293	#addi x5 x5 1	addi x5,x5,1
# 0x14	0xFF1FF0EF	#jal x1 -16	jal x1, loop
# 0x0	0x008000EF	#jal x1 8	jal x1,l
# 0x4	0x01C0006F	#jal x0 28	jal x0,exit
# 0x8	0xFFC10113	#addi x2 x2 -4	addi sp,sp,-4
# 0xc	0x00112023	#sw x1 0(x2)	sw x1,0(sp)
# 0x10	0x03200313	#addi x6 x0 50	addi x6,x0,50
# 0x14	0x00012083	#lw x1 0(x2)	lw x1,0(sp)
# 0x18	0x00410113	#addi x2 x2 4	addi sp,sp,4
# 0x1c	0x00008067	#jalr x0 x1 0	jalr x0,x1,0
# 0x20 0x11
# 0x0	0x10000517	#auipc x10 65536	lw x10, n
# 0x4	0x00052503	#lw x10 0(x10)	lw x10, n
# 0x8	0x008000EF	#jal x1 8	jal x1, fact
# 0xc	0x0400006F	#jal x0 64	jal x0, exit
# 0x10	0x00100293	#addi x5 x0 1	addi x5, x0, 1
# 0x14	0x00A2C663	#blt x5 x10 12	blt x5, x10, l1 #if n>1
# 0x18	0x00100513	#addi x10 x0 1	addi x10, x0, 1 #return 1
# 0x1c	0x00008067	#jalr x0 x1 0	jalr x0, x1, 0
# 0x20	0xFF810113	#addi x2 x2 -8	addi sp, sp, -8
# 0x24	0x00A12023	#sw x10 0(x2)	sw x10, 0(sp) #store return address and function parameter on stack
# 0x28	0x00112223	#sw x1 4(x2)	sw x1, 4(sp)
# 0x2c	0xFFF50513	#addi x10 x10 -1	addi x10, x10, -1 #n=n-1
# 0x30	0xFE1FF0EF	#jal x1 -32	jal x1, fact #fact(n-1)
# 0x34	0x00050313	#addi x6 x10 0	addi x6, x10, 0
# 0x38	0x00012503	#lw x10 0(x2)	lw x10, 0(sp)
# 0x3c	0x00412083	#lw x1 4(x2)	lw x1, 4(sp)
# 0x40	0x00810113	#addi x2 x2 8	addi sp, sp, 8
# 0x44	0x02650533	#mul x10 x10 x6	mul x10, x10, x6
# 0x48	0x00008067	#jalr x0 x1 0	jalr x0, x1, 0
# 0x4C 0x11
# lui x4,0x10000
# sw x4,0(x4)
0x0	0x10000537	#lui x10 65536	li x10,0x10000004
0x4	0x00450513	#addi x10 x10 4	li x10,0x10000004
0x8	0xFF1EE2B7	#lui x5 1044974	li x5,0xff1edfff
0xc	0xFFF28293	#addi x5 x5 -1	li x5,0xff1edfff
0x10	0x00552023	#sw x5 0(x10)	sw x5,0(x10)
0x14 0x11