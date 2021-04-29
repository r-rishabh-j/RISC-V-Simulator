print("RISC-V 32I simulator")
pipelining=int(input("Pipelining knob, 1 for pipelined, 0 for non pipelined: "))
if pipelining not in [0,1]:
    print("Wrong knob")
    sys.exit()

if pipelining==0:
    import main_non_pipelined
else:
    forwarding=int(input("Data Forwarding knob, 1 for ON, 0 for OFF: "))
    if forwarding not in [0,1]:
        print("Wrong knob")
        sys.exit()
    if forwarding==1:
        import main_forwarding
    else:
        import main_stall
    # print_reg_file=int(input("Printing the register file at the end of each cycle, 1 for ON, 0 for OFF: "))
    # if print_reg_file not in [0,1]:
    #     print("Wrong knob")
    #     sys.exit()
    # print_buff_file=int(input("Printing the pipeline buffer at the end of each cycle, 1 for ON, 0 for OFF: "))
    # if print_reg_file not in [0,1]:
    #     print("Wrong knob")
    #     sys.exit()
    # print_nth_buff=int(input("Specific instruction: 0 for off, instruction for on: "))
    # if print_nth_buff<0:
    #     print("Wrong knob")
    #     sys.exit()


