import sys

def runMain(pipeline):
    #print("RISC-V 32I simulator")
    #pipelining=int(input("Pipelining knob, 1 for pipelined, 0 for non pipelined: "))
    #if pipelining not in [0,1]:
        #print("Wrong knob")
        #sys.exit()

    if pipeline==0:
        import main_non_pipelined
    else:
        #forwarding=int(input("Data Forwarding knob, 1 for ON, 0 for OFF: "))
        #if forwarding not in [0,1]:
            #print("Wrong knob")
            #sys.exit()
        if pipeline==2:
            import main_forwarding
        else:
            import main_stall
