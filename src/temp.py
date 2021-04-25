MtoE=False # booleans to indicate data forwarding in the end of the same cycle, then set it to false
EtoD=False
EtoE=False
MtoM=False

def fetch(stage):
    # to do here
    # if terminate==1, return
    # operation queue will be used in the buffer update stage, not here.
    # fetch the instruction using the value in PC
    # compare it to BTB to check if that is a branch/jump. If it is, update PC to the target.
    # remember to enqueue the PC into the decode_PC_queue

def decode(stage):
    # if terminate==1, return
    # check the operation queue. If empty, then operate. Else, don't operate and pop.
    if(!control_module.decode_deque_signal())
    {
    	# decode stage is inactive. Perform other tasks  
    }
    # decode the instruction first in the IR
    control_module.decode(registers.ReadIR(),IAGmodule.PC)
    # check for hazards using the hazard table.
    hazard_code=hazard_module.check_dependance() # tentative !!
    # if hazard, perform corrective measures here and return. Do not execute further code
    if data_hazard:
      # code here for data hazard
      return
    # check for branch misprediction here
    # read the registers or PC or forwarded value here and update RA and RB with those values. Use control signals for MuxA and MuxB to set them!!!!
    # code for executing ALU for branch misprediction here.
    if not_jump_instruction:
    	control_module.ALUexecute(control_module.ALUOp, ALU_control_for_branch, RA, RB)
    # use branch prediction from the buffer
    if branch_misprediction: 
      # code here for handling branch misprediction
      control_module.execute_set_operate()
      control_module.memory_set_operate()
	  control_module.register_set_operate()
      return 
    # push NOPs whenever needed, call the exexute_set_NOP etc methods is ControlModule according to hazard code
    # if misprediction, perform corrective measures here and return if necessary follow steps given in documentation to resolve the hazard by stalling/data forwarding.
    # in case of jalr, compute effective address and update decode_output_PC_temp by that value.
    # if all good, push the decoded the signals into the queues.
    
    control_module.execute_set_operate()
    control_module.memory_set_operate()
	control_module.register_set_operate()
#MUXA, MUXB functionality needs to be implemented w/o the muxes!!!
def execute(stage): # ALU
    # dequeue from the control signals. Check if we need to operate or not
    #False == NOP, 
    if(!control_module.execute_deque_signal()){ # this function returns False if memory is in NOP. Also, all control_module.ALUop, etc are updated to 0 in case of NOP, or correct value if OP
    	# perform other tasks and return
    }
	# can use control_module.ALUop etc directly to use as arguments to ALU.
    ALUmodule.ALUexecute(control_module.ALUOp, control_module.ALUcontrol,buffer.getRA, buffer.getRB)
    buffer.setRZ(ALUmodule.output32)	#simple execution
    #add this code at the end of cycle
    #if(EtoE){
      #buffer.set
    #}  
    
    
def mem_access(stage):
    # dequeue from the control signals. Check if we need to operate or not
    if(!control_module.memory_deque_signal()) # this function returns False if memory is in NOP. Also, all control_module.MemRead, etc are updated to 0 in case of NOP, or correct value if OP
    {
      # perform other tasks and return
    }
    # acess memory and update temp memory buffers (RM_temp)
    memory.AccessMemory(control_module.MemRead, control_module.MemWrite, buffer.getRZ(), control_module.BytesToAccess, buffer.getRM()) # why RMtemp? RM is updated at the end of cycle
    # check forwarding
    if len(control_module.mem_ForwardQueue) != 0:
    {
      # check forwarding code
      # if MtoE
      MtoE = True
      # if MtoM
      MtoM = True
      buffer.setRMtemp(memory.MDR) # RM is updated to MDR of memory in case of M to M forwarding
    }
    # using MuxYSelect, set value of RYtemp
    if control_module.MuxYSelect == 0:
      buffer.RYtemp = buffer.getRZ()
    elif control_module.MuxYSelect == 1:
      buffer.RYtemp = memory.MDR
    elif control_module.MuxYSelect == 2:
      buffer.RYtemp = #P C Buffer use karun ? ya IAG module ka PC 
    # set RYtemp according to values and MuxY control
	
    
def reg_writeback(stage):
    # dequeue from the control signals. Check if we need to operate or not

def buffer_update():

def RunSim():
    clock=1
    while(True):
        # run the stages here, preferably in reverse order.
        # update the buffers in the end