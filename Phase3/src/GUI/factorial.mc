#data
~data
0x10000000 0x5
#text
~text
# 0x0	0x0440006F	#jal x0 68	j main
# 0x4	0xFF810113	#addi x2 x2 -8	addi sp sp -8
# 0x8	0x00112023	#sw x1 0(x2)	sw x1 0(sp)
# 0xc	0x00A12223	#sw x10 4(x2)	sw x10 4(sp) 
# 0x10	0x00100A93	#addi x21 x0 1	li x21 1
# 0x14	0x00AA9863	#bne x21 x10 16	bne x21 x10 l1 
# 0x18	0x00100513	#addi x10 x0 1	li x10 1
# 0x1c	0x00810113	#addi x2 x2 8	addi sp sp 8 
# 0x20	0x00008F67	#jalr x30 x1 0	jalr x30 x1 0
# 0x24	0x00412303	#lw x6 4(x2)	lw x6 4(sp) 
# 0x28	0xFFF30513	#addi x10 x6 -1	addi x10 x6 -1
# 0x2c	0xFD9FF0EF	#jal x1 -40	jal x1 fac
# 0x30	0x00412303	#lw x6 4(x2)	lw x6 4(sp) 
# 0x34	0x02650533	#mul x10 x10 x6	mul x10 x10 x6
# 0x38	0x00012083	#lw x1 0(x2)	lw x1 0(sp) 
# 0x3c	0x00810113	#addi x2 x2 8	addi sp sp 8 
# 0x40	0x00008F67	#jalr x30 x1 0	jalr x30 x1 0
# 0x44	0x10000517	#auipc x10 65536	lw x10 var1
# 0x48	0xFBC52503	#lw x10 -68(x10)	lw x10 var1
# 0x4c	0xFB9FF0EF	#jal x1 -72	jal x1 fac
# 0x50    0x11            #terminate
0x0	0x0440006F	#jal x0 68	j main
0x4	0xFF810113	#addi x2 x2 -8	addi sp sp -8
0x8	0x00112023	#sw x1 0(x2)	sw x1 0(sp)
0xc	0x00A12223	#sw x10 4(x2)	sw x10 4(sp) ## we have loaded n = x10 in stack because it is bound to change in a recursive call
0x10	0x00100A93	#addi x21 x0 1	li x21 1
0x14	0x00AA9863	#bne x21 x10 16	bne x21 x10 l1 ## if n=1
0x18	0x00100513	#addi x10 x0 1	li x10 1
0x1c	0x00810113	##addi x2 x2 8	addi sp sp 8 ## freeing the stack space
0x20	0x00008F67	#jalr x30 x1 0	jalr x30 x1 0
0x24	0x00412303	#lw x6 4(x2)	lw x6 4(sp) ## loading n in x6
0x28	0xFFF30513	#addi x10 x6 -1	addi x10 x6 -1
0x2c	0xFD9FF0EF	#jal x1 -40	jal x1 fac
0x30	0x00412303	#lw x6 4(x2)	lw x6 4(sp) ## loading n in x6 because x10 now has the value (n-1)!
0x34	0x02650533	#mul x10 x10 x6	mul x10 x10 x6
0x38	0x00012083	#lw x1 0(x2)	lw x1 0(sp) ## loading x1 becuase this was most certainly changed by several function calls ...
0x3c	0x00810113	#addi x2 x2 8	addi sp sp 8 ## now freeing up the stack and updating stack pointer
0x40	0x00008F67	#jalr x30 x1 0	jalr x30 x1 0
0x44	0x10000517	#auipc x10 65536	lw x10 var1
0x48	0xFBC52503	#lw x10 -68(x10)	lw x10 var1
0x4c	0xFB9FF0EF	#jal x1 -72	jal x1 fac
0x50 0x11