from PyQt5 import QtCore, QtGui, QtWidgets
import importlib
import MachineCodeParser
import RunSim_forward
import RunSim_stall
import RunSim_non_pipelined
import sys
#MachineCodeParser.parser("temp_gui_instructions.mc")

pipeline = 0    #0 for non-pipelined, 1 for pipeline w/o forwarding, 2 for pipeline with forwarding

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("RISC-V-Simulator")
        MainWindow.resize(1390, 844)
        font = QtGui.QFont()
        font.setPointSize(11)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        #
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(640, 10, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.label_param1 = QtWidgets.QLabel(self.centralwidget)
        self.label_param1.setGeometry(QtCore.QRect(525, 100, 200, 25))
        self.label_param1.setObjectName("label_param1")
        self.line_edit1 = QtWidgets.QLineEdit(self.centralwidget)
        self.line_edit1.setGeometry(QtCore.QRect(725, 100, 100, 25))
        self.line_edit1.setObjectName("line_edit1")
        #self.line_edit1.returnPressed.connect(lambda: self.do_action_cache_size())

        self.label_param2 = QtWidgets.QLabel(self.centralwidget)
        self.label_param2.setGeometry(QtCore.QRect(525, 150, 200, 25))
        self.label_param2.setObjectName("label_param2")
        self.line_edit2 = QtWidgets.QLineEdit(self.centralwidget)
        self.line_edit2.setGeometry(QtCore.QRect(725, 150, 100, 25))
        self.line_edit2.setObjectName("line_edit2")
        #self.line_edit2.returnPressed.connect(lambda: self.do_action_block_size())

        self.label_param3 = QtWidgets.QLabel(self.centralwidget)
        self.label_param3.setGeometry(QtCore.QRect(525, 200, 200, 25))
        self.label_param3.setObjectName("label_param3")
        self.line_edit3 = QtWidgets.QLineEdit(self.centralwidget)
        self.line_edit3.setGeometry(QtCore.QRect(725, 200, 100, 25))
        self.line_edit3.setObjectName("line_edit3")
        #self.line_edit3.returnPressed.connect(lambda: self.do_action_associativity())
        self.label_param4 = QtWidgets.QLabel(self.centralwidget)
        self.label_param4.setGeometry(QtCore.QRect(525, 275, 200, 25))
        self.label_param4.setObjectName("label_param4")
        self.line_edit4 = QtWidgets.QLineEdit(self.centralwidget)
        self.line_edit4.setGeometry(QtCore.QRect(725, 275, 100, 25))
        self.line_edit4.setObjectName("line_edit4")

        self.label_param5 = QtWidgets.QLabel(self.centralwidget)
        self.label_param5.setGeometry(QtCore.QRect(525, 325, 200, 25))
        self.label_param5.setObjectName("label_param5")
        self.line_edit5 = QtWidgets.QLineEdit(self.centralwidget)
        self.line_edit5.setGeometry(QtCore.QRect(725, 325, 100, 25))
        self.line_edit5.setObjectName("line_edit5")

        self.label_param6 = QtWidgets.QLabel(self.centralwidget)
        self.label_param6.setGeometry(QtCore.QRect(525, 375, 200, 25))
        self.label_param6.setObjectName("label_param6")
        self.line_edit6 = QtWidgets.QLineEdit(self.centralwidget)
        self.line_edit6.setGeometry(QtCore.QRect(725, 375, 100, 25))
        self.line_edit6.setObjectName("line_edit6")

        self.radiobutton_pipeline_no_fwd = QtWidgets.QRadioButton(self.centralwidget)
        self.radiobutton_pipeline_no_fwd.setGeometry(QtCore.QRect(550, 450, 225, 50))
        self.radiobutton_pipeline_no_fwd.toggled.connect(self.pipeline_no_fwd_selected)

        self.radiobutton_pipeline_fwd = QtWidgets.QRadioButton(self.centralwidget)
        self.radiobutton_pipeline_fwd.setGeometry(QtCore.QRect(550, 500, 225, 50))
        self.radiobutton_pipeline_fwd.toggled.connect(self.pipeline_fwd_selected)

        self.radiobutton_non_pipeline = QtWidgets.QRadioButton(self.centralwidget)
        self.radiobutton_non_pipeline.setGeometry(QtCore.QRect(550, 550, 225, 50))
        self.radiobutton_non_pipeline.toggled.connect(self.non_pipeline_selected)


        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(20, 50, 451, 711))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(200, 10, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        #self.MachineCode = QtWidgets.QTextBrowser(self.frame)
        #self.MachineCode.setGeometry(QtCore.QRect(0, 40, 511, 681))
        #self.MachineCode.setReadOnly(False)
        #self.MachineCode.setAcceptRichText(False)
        #self.MachineCode.setLineWrapMode(False)
        #self.MachineCode.setObjectName("MachineCode")
        #
        self.tableWidget = QtWidgets.QTableWidget(self.frame)
        self.tableWidget.setGeometry(QtCore.QRect(20, 40, 411, 671))
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setObjectName("tableWidget")
        #

        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(930, 50, 451, 711))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label_4 = QtWidgets.QLabel(self.frame_3)
        self.label_4.setGeometry(QtCore.QRect(200, 10, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.tableWidget2 = QtWidgets.QTableWidget(self.frame_3)
        self.tableWidget2.setGeometry(QtCore.QRect(20, 40, 411, 671))
        self.tableWidget2.setRowCount(0)
        self.tableWidget2.setColumnCount(0)
        self.tableWidget2.setObjectName("tableWidget2")
        #
        self.Run = QtWidgets.QPushButton(self.centralwidget)
        self.Run.setGeometry(QtCore.QRect(640, 740, 141, 41))
        self.Run.setObjectName("Run")
        self.Step = QtWidgets.QPushButton(self.centralwidget)
        self.Step.setGeometry(QtCore.QRect(640, 680, 141, 41))
        self.Step.setObjectName("Step")
        self.Assemble = QtWidgets.QPushButton(self.centralwidget)
        self.Assemble.setGeometry(QtCore.QRect(640, 620, 141, 41))
        self.Assemble.setObjectName("Assemble")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1390, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # running button
        self.Run.clicked.connect(self.run)
        self.Assemble.clicked.connect(self.assemble)
        self.Step.clicked.connect(self.step)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("RISC-V-Simulator", "RISC-V-Simulator"))
        self.label.setText(_translate("RISC-V-Simulator", "RISC-V SIMULATOR"))
        self.label_2.setText(_translate("RISC-V-Simulator", "I$"))
        #self.label_3.setText(_translate("RISC-V-Simulator", "Registers"))
        self.label_4.setText(_translate("RISC-V-Simulator", "D$"))

        self.label_param1.setText(_translate("RISC-V-Simulator", "I$ Cache Size (Bytes)"))
        self.label_param2.setText(_translate("RISC-V-Simulator", "I$ Block Size (Bytes)"))
        self.label_param3.setText(_translate("RISC-V-Simulator", "I$ Associativity"))
        self.label_param4.setText(_translate("RISC-V-Simulator", "D$ Cache Size (Bytes)"))
        self.label_param5.setText(_translate("RISC-V-Simulator", "D$ Block Size (Bytes)"))
        self.label_param6.setText(_translate("RISC-V-Simulator", "D$ Associativity"))

        self.radiobutton_pipeline_fwd.setText(_translate("RISC-V-Simulator", "Pipelined with Forwarding"))
        self.radiobutton_pipeline_no_fwd.setText(_translate("RISC-V-Simulator", "Pipelined without Forwarding"))
        self.radiobutton_non_pipeline.setText(_translate("RISC-V-Simulator", "Non-Pipelined"))

        self.Run.setText(_translate("RISC-V-Simulator", "RUN"))
        self.Step.setText(_translate("RISC-V-Simulator", "STEP"))
        self.Assemble.setText(_translate("RISC-V-Simulator", "ASSEMBLE"))

    def update_inst_cache(self, dic):
        #cache_list = list of sets(list of blocks)
        #maintain a non empty set boolean!!!??!!
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 300)
        #self.tableWidget.setColumnWidth(2, 150)

        self.tableWidget.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("Tag"))
        self.tableWidget.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("Contents"))
        #self.tableWidget.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem("Contents"))

        i=0
        for key, value in dic.items():
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            self.tableWidget.setItem(self.tableWidget.rowCount()-1, 0,
                                     QtWidgets.QTableWidgetItem(str(key)))
            s = [str(i) for i in value]
            self.tableWidget.setItem(self.tableWidget.rowCount()-1, 1,
                                     QtWidgets.QTableWidgetItem(" | ".join(s)))
            print(key, "|".join(s))
            #print(key, value)


    def update_data_cache(self, dic):
        #cache_list = list of sets(list of blocks)
        #maintain a non empty set boolean!!!??!!
        self.tableWidget2.setRowCount(0)
        self.tableWidget2.setColumnCount(2)
        self.tableWidget2.setColumnWidth(0, 100)
        self.tableWidget2.setColumnWidth(1, 300)
        #self.tableWidget2.setColumnWidth(2, 150)

        self.tableWidget2.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("Tag"))
        self.tableWidget2.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("Contents"))
        #self.tableWidget2.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem("Contents"))

        i=0
        for key, value in dic.items():
            self.tableWidget2.insertRow(self.tableWidget2.rowCount())
            self.tableWidget2.setItem(self.tableWidget2.rowCount()-1, 0,
                                     QtWidgets.QTableWidgetItem(str(key)))
            s = [str(i) for i in value]
            self.tableWidget2.setItem(self.tableWidget2.rowCount()-1, 1,
                                     QtWidgets.QTableWidgetItem(" | ".join(s)))
            print(key, "|".join(s))

    def pipeline_no_fwd_selected(self, selected):   #without data forwarding
        if selected:
            global pipeline
            pipeline = 1

    def pipeline_fwd_selected(self, selected):   #with data forwarding
        if selected:
            global pipeline
            pipeline = 2

    def non_pipeline_selected(self, selected):
        if selected:
            global pipeline
            pipeline = 0

    def assemble(self):
        # f = open("cache_specs.txt", "w")
        # f.write(self.line_edit1.text()+" "+self.line_edit2.text()+" "+self.line_edit3.text())
        # f.close()
        importlib.reload(RunSim_forward)
        importlib.reload(RunSim_stall)
        importlib.reload(RunSim_non_pipelined)
        importlib.reload(MachineCodeParser)
        MachineCodeParser.parser(sys.argv[1])
        RunSim_forward.memory.InitMemory(MachineCodeParser.PC_INST, MachineCodeParser.DATA, int(self.line_edit1.text()), int(self.line_edit2.text()), int(self.line_edit3.text()), int(self.line_edit4.text()), int(self.line_edit5.text()), int(self.line_edit6.text()))
        RunSim_stall.memory.InitMemory(MachineCodeParser.PC_INST, MachineCodeParser.DATA, int(self.line_edit1.text()), int(self.line_edit2.text()), int(self.line_edit3.text()), int(self.line_edit4.text()), int(self.line_edit5.text()), int(self.line_edit6.text()))
        RunSim_non_pipelined.memory.InitMemory(MachineCodeParser.PC_INST, MachineCodeParser.DATA, int(self.line_edit1.text()), int(self.line_edit2.text()), int(self.line_edit3.text()), int(self.line_edit4.text()), int(self.line_edit5.text()), int(self.line_edit6.text()))

    def padhexa(self, s):
        return '0x' + s[2:].zfill(8)

    def run(self):
        if pipeline==0:
            RunSim_non_pipelined.RunSim(1,1)
        if pipeline==1:
            RunSim_stall.RunSim(1,1)
        if pipeline==2:
            RunSim_forward.RunSim(1,1)
        if pipeline==0:
            self.update_inst_cache(RunSim_non_pipelined.memory.text_module.cache_module.cache_dict)
            self.update_data_cache(RunSim_non_pipelined.memory.data_module.cache_module.cache_dict)
            #print(RunSim_non_pipelined.memory.text_module.cache_module.cache_dict)
        if pipeline==1:
            self.update_inst_cache(RunSim_stall.memory.text_module.cache_module.cache_dict)
            self.update_data_cache(RunSim_stall.memory.data_module.cache_module.cache_dict)
            #print(RunSim_stall.memory.text_module.cache_module.cache_dict)
        if pipeline==2:
            self.update_inst_cache(RunSim_forward.memory.text_module.cache_module.cache_dict)
            self.update_data_cache(RunSim_forward.memory.data_module.cache_module.cache_dict)
            #print(RunSim_forward.memory.text_module.cache_module.cache_dict)
        #def print_reg(arr):  # input is numpy array
        with open(f"RegisterDump.mc", "w") as fileReg:
            for i in range(32): # for all 32 registers
                fileReg.write(f"x{i} ")  # print address of register for eg. x5
                if (RunSim_forward.registers.reg[i] >= 0):
                    fileReg.write(self.padhexa(hex(RunSim_forward.registers.reg[i])).upper().replace('X', 'x'))
                else:
                    reg = RunSim_forward.registers.reg[i] & 0xffffffff  # signed
                    fileReg.write(hex(reg).upper().replace('X', 'x'))
                fileReg.write("\n")

        #dumping memory
        with open(f"MemoryDump.mc", "w") as fileMem:  # input is dictionary with key as address and value as data
            lst = []  # stores keys present in dictionary
            temp_lst = []  # stores base address
            for key in RunSim_forward.memory.data_module.memory:
                lst.append(key)
            lst.sort()
            for x in lst:
                temp = x - (x % 4)  # storing base address in temp
                if temp not in temp_lst:  # if base address not present in temp_list , then append it
                    temp_lst.append(temp)
            temp_lst.sort()
            for i in temp_lst:
                fileMem.write(f"{(self.padhexa(hex(i)).upper().replace('X', 'x'))} ")  # printing base address
                if i in lst:
                    fileMem.write(f"{(self.padhexa(hex(RunSim_forward.memory.data_module.memory[i])).upper())[8:]} " )  # if key in dictionary, print its data
                else:
                    fileMem.write("00 ")  # if key not in dictionary, print 00
                if (i + 1) in lst:
                    fileMem.write(f"{(self.padhexa(hex(RunSim_forward.memory.data_module.memory[i + 1])).upper())[8:]} ")
                else:
                    fileMem.write("00 ")
                if (i + 2) in lst:
                    fileMem.write(f"{(self.padhexa(hex(RunSim_forward.memory.data_module.memory[i + 2])).upper())[8:]} ")
                else:
                    fileMem.write("00 ")
                if (i + 3) in lst:
                    fileMem.write(f"{(self.padhexa(hex(RunSim_forward.memory.data_module.memory[i + 3])).upper())[8:]} ")
                else:
                    fileMem.write("00  ")
                fileMem.write("\n")  # new line
            lst = []  # stores keys present in dictionary
            temp_lst = []
            for key in RunSim_forward.memory.text_module.memory:
                lst.append(key)
            lst.sort()
            for x in lst:
                temp = x - (x % 4)  # storing base address in temp
                if temp not in temp_lst:  # if base address not present in temp_list , then append it
                    temp_lst.append(temp)
            temp_lst.sort()
            for i in temp_lst:
                fileMem.write(f"{(self.padhexa(hex(i)).upper().replace('X', 'x'))} ")  # printing base address
                if i in lst:
                    fileMem.write(f"{(self.padhexa(hex(RunSim_forward.memory.text_module.memory[i])).upper())[8:]} " )  # if key in dictionary, print its data
                else:
                    fileMem.write("00 ")  # if key not in dictionary, print 00
                if (i + 1) in lst:
                    fileMem.write(f"{(self.padhexa(hex(RunSim_forward.memory.text_module.memory[i + 1])).upper())[8:]} ")
                else:
                    fileMem.write("00 ")
                if (i + 2) in lst:
                    fileMem.write(f"{(self.padhexa(hex(RunSim_forward.memory.text_module.memory[i + 2])).upper())[8:]} ")
                else:
                    fileMem.write("00 ")
                if (i + 3) in lst:
                    fileMem.write(f"{(self.padhexa(hex(RunSim_forward.memory.text_module.memory[i + 3])).upper())[8:]} ")
                else:
                    fileMem.write("00  ")
                fileMem.write("\n")  # new line
        print("\033[1;92mRegister and memory outputs written in RegisterDump.mc and MemoryDump.mc respectively\033[0m")
        importlib.reload(RunSim_forward)
        importlib.reload(RunSim_stall)
        importlib.reload(RunSim_non_pipelined)
        importlib.reload(MachineCodeParser)

    def step(self):
        if pipeline==0:
            RunSim_non_pipelined.RunSim_step(1,1)
        if pipeline==1:
            RunSim_stall.RunSim_step(1,1)
        if pipeline==2:
            RunSim_forward.RunSim_step(1,1)
        if pipeline==0:
            self.update_inst_cache(RunSim_non_pipelined.memory.text_module.cache_module.cache_dict)
            #print(RunSim_non_pipelined.memory.text_module.cache_module.cache_dict)
        if pipeline==1:
            self.update_inst_cache(RunSim_stall.memory.text_module.cache_module.cache_dict)
            #print(RunSim_stall.memory.text_module.cache_module.cache_dict)
        if pipeline==2:
            self.update_inst_cache(RunSim_forward.memory.text_module.cache_module.cache_dict)
            #print(RunSim_forward.memory.text_module.cache_module.cache_dict)
        #def print_reg(arr):  # input is numpy array
        with open(f"RegisterDump.mc", "w") as fileReg:
            for i in range(32): # for all 32 registers
                fileReg.write(f"x{i} ")  # print address of register for eg. x5
                if (RunSim_forward.registers.reg[i] >= 0):
                    fileReg.write(self.padhexa(hex(RunSim_forward.registers.reg[i])).upper().replace('X', 'x'))
                else:
                    reg = RunSim_forward.registers.reg[i] & 0xffffffff  # signed
                    fileReg.write(hex(reg).upper().replace('X', 'x'))
                fileReg.write("\n")

        #dumping memory
        with open(f"MemoryDump.mc", "w") as fileMem:  # input is dictionary with key as address and value as data
            lst = []  # stores keys present in dictionary
            temp_lst = []  # stores base address
            for key in RunSim_forward.memory.data_module.memory:
                lst.append(key)
            lst.sort()
            for x in lst:
                temp = x - (x % 4)  # storing base address in temp
                if temp not in temp_lst:  # if base address not present in temp_list , then append it
                    temp_lst.append(temp)
            temp_lst.sort()
            for i in temp_lst:
                fileMem.write(f"{(self.padhexa(hex(i)).upper().replace('X', 'x'))} ")  # printing base address
                if i in lst:
                    fileMem.write(f"{(self.padhexa(hex(RunSim_forward.memory.data_module.memory[i])).upper())[8:]} " )  # if key in dictionary, print its data
                else:
                    fileMem.write("00 ")  # if key not in dictionary, print 00
                if (i + 1) in lst:
                    fileMem.write(f"{(self.padhexa(hex(RunSim_forward.memory.data_module.memory[i + 1])).upper())[8:]} ")
                else:
                    fileMem.write("00 ")
                if (i + 2) in lst:
                    fileMem.write(f"{(self.padhexa(hex(RunSim_forward.memory.data_module.memory[i + 2])).upper())[8:]} ")
                else:
                    fileMem.write("00 ")
                if (i + 3) in lst:
                    fileMem.write(f"{(self.padhexa(hex(RunSim_forward.memory.data_module.memory[i + 3])).upper())[8:]} ")
                else:
                    fileMem.write("00  ")
                fileMem.write("\n")  # new line
            lst = []  # stores keys present in dictionary
            temp_lst = []
            for key in RunSim_forward.memory.text_module.memory:
                lst.append(key)
            lst.sort()
            for x in lst:
                temp = x - (x % 4)  # storing base address in temp
                if temp not in temp_lst:  # if base address not present in temp_list , then append it
                    temp_lst.append(temp)
            temp_lst.sort()
            for i in temp_lst:
                fileMem.write(f"{(self.padhexa(hex(i)).upper().replace('X', 'x'))} ")  # printing base address
                if i in lst:
                    fileMem.write(f"{(self.padhexa(hex(RunSim_forward.memory.text_module.memory[i])).upper())[8:]} " )  # if key in dictionary, print its data
                else:
                    fileMem.write("00 ")  # if key not in dictionary, print 00
                if (i + 1) in lst:
                    fileMem.write(f"{(self.padhexa(hex(RunSim_forward.memory.text_module.memory[i + 1])).upper())[8:]} ")
                else:
                    fileMem.write("00 ")
                if (i + 2) in lst:
                    fileMem.write(f"{(self.padhexa(hex(RunSim_forward.memory.text_module.memory[i + 2])).upper())[8:]} ")
                else:
                    fileMem.write("00 ")
                if (i + 3) in lst:
                    fileMem.write(f"{(self.padhexa(hex(RunSim_forward.memory.text_module.memory[i + 3])).upper())[8:]} ")
                else:
                    fileMem.write("00  ")
                fileMem.write("\n")  # new line

    # def run(self):

    #     #import temp_main
    #     # code to start running the code
    #     # code to add data in register text Box
    #     #code = self.MachineCode.toPlainText()
    #     #print(code)
    #     #fhand = open("gui_instructions.mc", 'r')
    #     #fhand.write(code)
    #     #fhand.close()


    #     #print(MachineCodeParser.PC_INST)
    #     # program load
    #     #RiscSim.memory.InitMemory(MachineCodeParser.PC_INST)
    #     # Run the simulator
    #     #RiscSim.RunSim()
    #     ###temp_main.runMain()
    #     # reg = np.array([1, -2, 3])
    #     value = self.line_edit1.text()
    #     print(int(value))
    #     value = self.line_edit2.text()
    #     print(int(value))
    #     value = self.line_edit3.text()
    #     print(int(value))
    #     print(pipeline)


    #     # f = open("cache_specs.txt", "w")
    #     # f.write(self.line_edit1.text()+" "+self.line_edit2.text()+" "+self.line_edit3.text())
    #     # f.close()

    #     #temp_main.runMain(pipeline)
    #     if pipeline == 0:
    #         import RunSim_non_pipelined
    #         RunSim_non_pipelined.memory.InitMemory(MachineCodeParser.PC_INST, MachineCodeParser.DATA)
    #         RunSim_non_pipelined.RunSim()
    #         #add dumping functions
    #         self.update_inst_cache(RunSim_non_pipelined.memory.text_module.cache_module.cache_dict)
            #self.update_data_cache(RunSim_non_pipelined.memory.data_module.cache_module.cache_dict)


        # #code to add memory in memory text Box
        # dic = {19: 3, 4: 11, 6: 7, 241: 241}
        #self.update_memory(RiscSim.memory.memory_module.memory)
        #importlib.reload(temp_main)
        #importlib.reload(MachineCodeParser)




if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
