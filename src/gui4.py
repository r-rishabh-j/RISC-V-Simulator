# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui1.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import MachineCodeParser
import RiscSim


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1390, 844)
        font = QtGui.QFont()
        font.setPointSize(11)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(660, 10, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(20, 50, 521, 721))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(200, 10, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.MachineCode = QtWidgets.QTextBrowser(self.frame)
        self.MachineCode.setGeometry(QtCore.QRect(0, 40, 511, 681))
        self.MachineCode.setReadOnly(False)
        self.MachineCode.setAcceptRichText(False)
        self.MachineCode.setLineWrapMode(False)
        self.MachineCode.setObjectName("MachineCode")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(550, 50, 371, 681))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setGeometry(QtCore.QRect(150, 10, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.Registers = QtWidgets.QTextBrowser(self.frame_2)
        self.Registers.setGeometry(QtCore.QRect(30, 40, 331, 631))
        self.Registers.setObjectName("Registers")
        self.Registers.setAcceptRichText(True)
        self.Registers.setOpenExternalLinks(True)
        self.Registers.setText("")
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
        self.Memory = QtWidgets.QTextBrowser(self.frame_3)
        self.Memory.setGeometry(QtCore.QRect(20, 40, 411, 671))
        self.Memory.setObjectName("Memory")
        self.Run = QtWidgets.QPushButton(self.centralwidget)
        self.Run.setGeometry(QtCore.QRect(680, 740, 141, 41))
        self.Run.setObjectName("Run")
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

        #running button
        self.Run.clicked.connect(self.run)
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "RISC-V SIMULATOR"))
        self.label_2.setText(_translate("MainWindow", "Machine Code"))
        self.label_3.setText(_translate("MainWindow", "Registers"))
        self.label_4.setText(_translate("MainWindow", "Memory"))
        self.Run.setText(_translate("MainWindow", "RUN"))

    def padhexa(self, s):
        return '0x' + s[2:].zfill(8)

    def update_registers(self, arr):
        for i in range(32):
            text = "x"+str(i)
            # print address of register for eg. x5
            if arr[i] >= 0:
                self.Registers.append(text + "\t" + self.padhexa(hex(arr[i])))
            else:
                reg = arr[i] & 0xffffffff  # signed
                self.Registers.append(text + "\t" + hex(reg))

    def update_memory(self, dic):
        lst = []  # stores keys present in dictionary
        temp_lst = []  # stores base address
        for key in dic:
            lst.append(key)
        lst.sort()
        for x in lst:
            temp = x - (x % 4)  # storing base address in temp
            if temp not in temp_lst:  # if base address not present in temp_list , then append it
                temp_lst.append(temp)
        temp_lst.sort()
        for i in temp_lst:
            text = ""
            text = text + self.padhexa(hex(i)) # printing base address
            if i in lst:
                  # if data in dictionary
                text = text + "\t" +self.padhexa(hex(dic[i]))[8:]
            else:
                 # if data not in dictionary
                text = text + "\t" + "00"
            if (i + 1) in lst:

                text = text + " " + self.padhexa(hex(dic[i+1]))[8:]
            else:

                text = text + " " + "00"
            if (i + 2) in lst:

                text = text + " " + self.padhexa(hex(dic[i+2]))[8:]
            else:

                text = text + " " + "00"
            if (i + 3) in lst:

                text = text + " " + self.padhexa(hex(dic[i+3]))[8:]
            else:

                text = text + " " + "00"
            self.Memory.append(text)

    def run(self):
        #code to start running the code
        #code to add data in register text Box
        code=self.MachineCode.toPlainText()
        print(code)
        fhand=open("gui_instructions.mc",'w')
        fhand.write(code)
        fhand.close()

        MachineCodeParser.parser("gui_instructions.mc")
        print(MachineCodeParser.PC_INST)
       # program load
        RiscSim.memory.InitMemory(MachineCodeParser.PC_INST)
        #Run the simulator
        RiscSim.RunSim()
        # reg = np.array([1, -2, 3])
        self.update_registers(RiscSim.registers.reg)
        # #code to add memory in memory text Box
        #dic = {19: 3, 4: 11, 6: 7, 241: 241}
        self.update_memory(RiscSim.memory.memory_module.memory)

        with open(f"RegisterDump.mc", "w") as fileReg:
            for i in range(32): # for all 32 registers
                fileReg.write(f"x{i} ")  # print address of register for eg. x5
                if (RiscSim.registers.reg[i] >= 0):
                    fileReg.write(self.padhexa(hex(RiscSim.registers.reg[i])))
                else:
                    reg = RiscSim.registers.reg[i] & 0xffffffff  # signed
                    fileReg.write(hex(reg))
                fileReg.write("\n")

# dumping memory
        with open(f"MemoryDump.mc", "w") as fileMem:  # input is dictionary with key as address and value as data
            lst = []  # stores keys present in dictionary
            temp_lst = []  # stores base address
            for key in RiscSim.memory.memory_module.memory:
                lst.append(key)
            lst.sort()
            for x in lst:
                temp = x - (x % 4)  # storing base address in temp
                if temp not in temp_lst:  # if base address not present in temp_list , then append it
                    temp_lst.append(temp)
            temp_lst.sort()
            for i in temp_lst:
                fileMem.write(f"{self.padhexa(hex(i))} ")  # printing base address
                if i in lst:
                    fileMem.write(f"{self.padhexa(hex(RiscSim.memory.memory_module.memory[i]))[8:]} " )  # if key in dictionary, print its data
                else:
                    fileMem.write("00  ")  # if key not in dictionary, print 00
                if (i + 1) in lst:
                    fileMem.write(f"{self.padhexa(hex(RiscSim.memory.memory_module.memory[i + 1]))[8:]} ")
                else:
                    fileMem.write("00  ")
                if (i + 2) in lst:
                    fileMem.write(f"{self.padhexa(hex(RiscSim.memory.memory_module.memory[i + 2]))[8:]} ")
                else:
                    fileMem.write("00  ")
                if (i + 3) in lst:
                    fileMem.write(f"{self.padhexa(hex(RiscSim.memory.memory_module.memory[i + 3]))[8:]} ")
                else:
                    fileMem.write("00  ")
                fileMem.write("\n")  # new line
        print("Files dump successfully")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
