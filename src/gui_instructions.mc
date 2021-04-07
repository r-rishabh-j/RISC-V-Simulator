0x10000000 0xf
0x0	0x10000597	#auipc x11 65536	lw x11,N
0x4	0x0005A583	#lw x11 0(x11)	lw x11,N
0x8	0x00300293	#addi x5 x0 3	li x5,3 #fib(n<3, 1 or 2)==1
0xc	0x008000EF	#jal x1 8	jal x1,fib
0x10	0x04C0006F	#jal x0 76	j EXIT
0x14	0x0455C063	#blt x11 x5 64	blt x11,x5,return
0x18	0xFFC10113	#addi x2 x2 -4	addi sp,sp,-4
0x1c	0x00112023	#sw x1 0(x2)	sw x1,0(sp)
0x20	0xFFF58593	#addi x11 x11 -1	addi x11,x11,-1
0x24	0xFF1FF0EF	#jal x1 -16	jal x1,fib
0x28	0xFFC10113	#addi x2 x2 -4	addi sp,sp,-4
0x2c	0x00912023	#sw x9 0(x2)	sw x9, 0(sp)
0x30	0xFFF58593	#addi x11 x11 -1	addi x11,x11,-1
0x34	0xFE1FF0EF	#jal x1 -32	jal x1,fib
0x38	0x00012603	#lw x12 0(x2)	lw x12,0(sp)
0x3c	0x00410113	#addi x2 x2 4	addi sp,sp,4
0x40	0x009604B3	#add x9 x12 x9	add x9,x12,x9
0x44	0x00258593	#addi x11 x11 2	addi x11,x11,2
0x48	0x00012083	#lw x1 0(x2)	lw x1,0(sp)
0x4c	0x00410113	#addi x2 x2 4	addi sp,sp,4
0x50	0x00008067	#jalr x0 x1 0	jalr x0,x1,0
0x54	0x00100493	#addi x9 x0 1	addi x9,x0,1
0x58	0x00008067	#jalr x0 x1 0	jalr x0,x1,0
0x5c    0x11