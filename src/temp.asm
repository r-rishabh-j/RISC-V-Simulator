.data 
var1: .word 12

.text 
j main

fac:
addi sp sp -8
sw x1 0(sp)
sw x10 4(sp)  ## we have loaded n = x10 in stack because it is bound to change in a recursive call 

li x21 1
bne x21 x10 l1 ## if n=1
li x10 1
addi sp sp 8 ## freeing the stack space 
jalr x30 x1 0

l1: # else 
lw x6 4(sp)  ## loading n in x6 
addi x10 x6 -1
jal x1 fac
lw x6 4(sp)  ## loading n in x6 because x10 now has the value (n-1)! 
mul x10 x10 x6
lw x1 0(sp)  ## loading x1 becuase this was most certainly changed by several function calls ...
addi sp sp 8 ## now freeing up the stack and updating stack pointer 
jalr x30 x1 0

main:
lw x10 var1
jal x1 fac