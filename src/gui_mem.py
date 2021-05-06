from PyQt5 import QtCore, QtGui, QtWidgets
import importlib

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
        self.tableWidget = QtWidgets.QTableWidget(self.frame_3)
        self.tableWidget.setGeometry(QtCore.QRect(20, 40, 411, 671))
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setObjectName("tableWidget")
        #
        self.Run = QtWidgets.QPushButton(self.centralwidget)
        self.Run.setGeometry(QtCore.QRect(640, 740, 141, 41))
        self.Run.setObjectName("Run")
        self.Step = QtWidgets.QPushButton(self.centralwidget)
        self.Step.setGeometry(QtCore.QRect(640, 680, 141, 41))
        self.Step.setObjectName("Step")
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

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("RISC-V-Simulator", "RISC-V-Simulator"))
        self.label.setText(_translate("RISC-V-Simulator", "RISC-V SIMULATOR"))
        self.label_2.setText(_translate("RISC-V-Simulator", "I$"))
        #self.label_3.setText(_translate("RISC-V-Simulator", "Registers"))
        self.label_4.setText(_translate("RISC-V-Simulator", "D$"))
        self.Run.setText(_translate("RISC-V-Simulator", "RUN"))
        self.Step.setText(_translate("RISC-V-Simulator", "STEP"))

    def run(self):
        import MachineCodeParser
        import temp_main
        # code to start running the code
        # code to add data in register text Box
        #code = self.MachineCode.toPlainText()
        #print(code)
        #fhand = open("gui_instructions.mc", 'r')
        #fhand.write(code)
        #fhand.close()

        MachineCodeParser.parser("temp_gui_instructions.mc")
        #print(MachineCodeParser.PC_INST)
        # program load
        #RiscSim.memory.InitMemory(MachineCodeParser.PC_INST)
        # Run the simulator
        #RiscSim.RunSim()
        ####temp_main.runMain()
        # reg = np.array([1, -2, 3])
        #self.update_registers(RiscSim.registers.reg)
        # #code to add memory in memory text Box
        # dic = {19: 3, 4: 11, 6: 7, 241: 241}
        #self.update_memory(RiscSim.memory.memory_module.memory)
        importlib.reload(temp_main)
        importlib.reload(MachineCodeParser)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
