# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import RunSim_forward
import RunSim_non_pipelined
import RunSim_stall
import importlib
import MachineCodeParser
import sys
import math

pipeline=0 # 0 for non-pipelined, 1 for pipeline w/o forwarding, 2 for pipeline with forwarding
error=True
finished=True
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgba(242, 242, 242,1);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1501, 951))
        self.tabWidget.setStyleSheet(MainWindow.styleSheet())
        # self.tabWidget.setStyleSheet("background-color: rgb(242, 242, 242);")
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.MachineCodeInput = QtWidgets.QPlainTextEdit(self.tab)
        self.MachineCodeInput.setFont(font)
        self.MachineCodeInput.setGeometry(QtCore.QRect(10, 40, 601, 851))
        self.MachineCodeInput.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.MachineCodeInput.setObjectName("MachineCodeInput")
        self.assemble_button = QtWidgets.QPushButton(self.tab)
        self.assemble_button.setGeometry(QtCore.QRect(680, 680, 121, 61))
        self.assemble_button.setStyleSheet("font: 13pt \"MS Shell Dlg 2\";\n" "background-color: rgb(154, 255, 140);")
        self.assemble_button.setObjectName("assemble_button")
        self.step_button = QtWidgets.QPushButton(self.tab)
        self.step_button.setGeometry(QtCore.QRect(680, 750, 121, 61))
        self.step_button.setStyleSheet("font: 13pt \"MS Shell Dlg 2\";\n"
"background-color: rgb(154, 255, 140);")
        self.step_button.setObjectName("step_button")
        self.run_button = QtWidgets.QPushButton(self.tab)
        self.run_button.setGeometry(QtCore.QRect(680, 820, 121, 61))
        self.run_button.setStyleSheet("font: 13pt \"MS Shell Dlg 2\";\n"
"background-color: rgb(154, 255, 140);")
        self.run_button.setObjectName("run_button")
        self.clock_display = QtWidgets.QLCDNumber(self.tab)
        self.clock_display.setGeometry(QtCore.QRect(660, 620, 161, 51))
        self.clock_display.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.clock_display.setObjectName("clock_display")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(190, 10, 241, 31))
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(700, 590, 81, 31))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setGeometry(QtCore.QRect(1020, 670, 241, 31))
        self.label_5.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label_5.setObjectName("label_5")
        self.pipe_forward_radio = QtWidgets.QRadioButton(self.tab)
        self.pipe_forward_radio.setGeometry(QtCore.QRect(630, 500, 231, 21))
        self.pipe_forward_radio.setStyleSheet("font: 11pt \"MS Shell Dlg 2\";")
        self.pipe_forward_radio.setObjectName("pipe_forward_radio")
        self.pipe_forward_radio.toggled.connect(self.pipeline_fwd_selected)
        self.pipe_no_forward_radio = QtWidgets.QRadioButton(self.tab)
        self.pipe_no_forward_radio.setGeometry(QtCore.QRect(630, 530, 221, 20))
        self.pipe_no_forward_radio.setStyleSheet("font: 11pt \"MS Shell Dlg 2\";")
        self.pipe_no_forward_radio.setObjectName("pipe_no_forward_radio")
        self.pipe_no_forward_radio.toggled.connect(self.pipeline_no_fwd_selected)
        self.no_pipe_radio = QtWidgets.QRadioButton(self.tab)
        self.no_pipe_radio.setGeometry(QtCore.QRect(630, 560, 161, 20))
        self.no_pipe_radio.setStyleSheet("font: 11pt \"MS Shell Dlg 2\";")
        self.no_pipe_radio.setObjectName("no_pipe_radio")
        self.no_pipe_radio.toggled.connect(self.non_pipeline_selected)
        self.tabWidget_2 = QtWidgets.QTabWidget(self.tab)
        self.tabWidget_2.setGeometry(QtCore.QRect(860, 0, 561, 661))
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.label_2 = QtWidgets.QLabel(self.tab_3)
        self.label_2.setGeometry(QtCore.QRect(160, 0, 241, 31))
        self.label_2.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.RegisterOutput = QtWidgets.QTableWidget(self.tab_3)
        self.RegisterOutput.setGeometry(QtCore.QRect(0, 30, 551, 601))
        self.RegisterOutput.setFont(font)
        self.RegisterOutput.setStyleSheet("background-color: rgb(255, 255, 255);")
        # self.RegisterOutput.setReadOnly(True)
        self.RegisterOutput.setRowCount(0)
        self.RegisterOutput.setColumnCount(0)
        self.RegisterOutput.setObjectName("RegisterOutput")

        self.tabWidget_2.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.label_3 = QtWidgets.QLabel(self.tab_4)
        self.label_3.setGeometry(QtCore.QRect(160, 0, 241, 31))
        self.label_3.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")
        #######
        self.MemoryOutput = QtWidgets.QTableWidget(self.tab_4)
        self.MemoryOutput.setGeometry(QtCore.QRect(0, 30, 551, 601))
        self.MemoryOutput.setStyleSheet("background-color: rgb(255, 255, 255);")
        # self.MemoryOutput.setReadOnly(True)
        self.MemoryOutput.setRowCount(0)
        self.MemoryOutput.setColumnCount(0)
        self.MemoryOutput.setFont(font)
        self.MemoryOutput.setObjectName("MemoryOutput")
        ########

        self.tabWidget_2.addTab(self.tab_4, "")
        font10 = QtGui.QFont()
        font10.setPointSize(10)
        self.Icache_size = QtWidgets.QLineEdit(self.tab)
        self.Icache_size.setGeometry(QtCore.QRect(740, 180, 81, 31))
        self.Icache_size.setObjectName("Icache_size")
        self.Icache_size.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Icache_size.setFont(font10)
        self.Dcache_size = QtWidgets.QLineEdit(self.tab)
        self.Dcache_size.setGeometry(QtCore.QRect(740, 360, 81, 31))
        self.Dcache_size.setObjectName("Dcache_size")
        self.Dcache_size.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Dcache_size.setFont(font10)
        self.Dcache_blocksize = QtWidgets.QLineEdit(self.tab)
        self.Dcache_blocksize.setGeometry(QtCore.QRect(740, 400, 81, 31))
        self.Dcache_blocksize.setObjectName("Dcache_blocksize")
        self.Dcache_blocksize.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Dcache_blocksize.setFont(font10)
        self.Dcache_assoc = QtWidgets.QLineEdit(self.tab)
        self.Dcache_assoc.setGeometry(QtCore.QRect(740, 440, 81, 31))
        self.Dcache_assoc.setObjectName("Dcache_assoc")
        self.Dcache_assoc.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Dcache_assoc.setFont(font10)
        self.Icache_blocksize = QtWidgets.QLineEdit(self.tab)
        self.Icache_blocksize.setGeometry(QtCore.QRect(740, 220, 81, 31))
        self.Icache_blocksize.setObjectName("Icache_blocksize")
        self.Icache_blocksize.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Icache_blocksize.setFont(font10)
        self.Icache_assoc = QtWidgets.QLineEdit(self.tab)
        self.Icache_assoc.setGeometry(QtCore.QRect(740, 260, 81, 31))
        self.Icache_assoc.setObjectName("Icache_assoc")
        self.Icache_assoc.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Icache_assoc.setFont(font10)
        self.label_8 = QtWidgets.QLabel(self.tab)
        self.label_8.setGeometry(QtCore.QRect(710, 140, 55, 21))
        self.label_8.setStyleSheet("font: 11pt \"MS Shell Dlg 2\";")
        self.label_8.setObjectName("label_8")
        self.label_10 = QtWidgets.QLabel(self.tab)
        self.label_10.setGeometry(QtCore.QRect(640, 180, 91, 20))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.tab)
        self.label_11.setGeometry(QtCore.QRect(710, 320, 55, 21))
        self.label_11.setStyleSheet("font: 11pt \"MS Shell Dlg 2\";")
        self.label_11.setObjectName("label_11")
        self.label_13 = QtWidgets.QLabel(self.tab)
        self.label_13.setGeometry(QtCore.QRect(640, 220, 100, 20))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.tab)
        self.label_14.setGeometry(QtCore.QRect(630, 260, 101, 20))
        self.label_14.setObjectName("label_14")
        self.label_12 = QtWidgets.QLabel(self.tab)
        self.label_12.setGeometry(QtCore.QRect(640, 360, 91, 20))
        self.label_12.setObjectName("label_12")
        self.label_15 = QtWidgets.QLabel(self.tab)
        self.label_15.setGeometry(QtCore.QRect(640, 400, 100, 20))
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.tab)
        self.label_16.setGeometry(QtCore.QRect(630, 440, 101, 20))
        self.label_16.setObjectName("label_16")
        self.console = QtWidgets.QPlainTextEdit(self.tab)
        self.console.setGeometry(QtCore.QRect(860, 700, 561, 191))
        self.console.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.console.setReadOnly(True)
        self.console.setObjectName("console")
        self.console.verticalScrollBar().setValue(0)
        self.console.setFont(font)
        self.label_4.raise_()
        self.label_5.raise_()
        self.label.raise_()
        self.MachineCodeInput.raise_()
        self.MachineCodeInput.setLineWrapMode(False)
        self.assemble_button.raise_()
        self.step_button.raise_()
        self.run_button.raise_()
        self.clock_display.raise_()
        self.pipe_forward_radio.raise_()
        self.pipe_no_forward_radio.raise_()
        self.no_pipe_radio.raise_()
        self.tabWidget_2.raise_()
        self.Icache_size.raise_()
        self.Dcache_size.raise_()
        self.Dcache_blocksize.raise_()
        self.Dcache_assoc.raise_()
        self.Icache_blocksize.raise_()
        self.Icache_assoc.raise_()
        self.label_8.raise_()
        self.label_10.raise_()
        self.label_11.raise_()
        self.label_13.raise_()
        self.label_14.raise_()
        self.label_12.raise_()
        self.label_15.raise_()
        self.label_16.raise_()
        self.console.raise_()
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.Icache_output = QtWidgets.QTableWidget(self.tab_2)
        self.Icache_output.setGeometry(QtCore.QRect(20, 40, 641, 631))
        self.Icache_output.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Icache_output.setRowCount(0)
        self.Icache_output.setColumnCount(0)
        # self.Icache_output.setReadOnly(True)
        self.Icache_output.setFont(font)
        self.Icache_output.setObjectName("Icache_output")
        ##########
        self.Dcache_output = QtWidgets.QTableWidget(self.tab_2)
        self.Dcache_output.setGeometry(QtCore.QRect(770, 40, 641, 631))
        self.Dcache_output.setStyleSheet("background-color: rgb(255, 255, 255);")
        # self.DcacheOutput.setReadOnly(True)
        self.Dcache_output.setRowCount(0)
        self.Dcache_output.setColumnCount(0)
        self.Dcache_output.setFont(font)
        self.Dcache_output.setObjectName("DcacheOutput")
        ##########
        self.label_6 = QtWidgets.QLabel(self.tab_2)
        self.label_6.setGeometry(QtCore.QRect(190, 0, 241, 31))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.tab_2)
        self.label_7.setGeometry(QtCore.QRect(990, 0, 241, 31))
        self.label_7.setObjectName("label_7")
        self.Icache_stats = QtWidgets.QPlainTextEdit(self.tab_2)
        self.Icache_stats.setGeometry(QtCore.QRect(20, 690, 361, 201))
        self.Icache_stats.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Icache_stats.setReadOnly(True)
        self.Icache_stats.setFont(font)
        self.Icache_stats.setObjectName("Icache_stats")
        self.Dcache_stats = QtWidgets.QPlainTextEdit(self.tab_2)
        self.Dcache_stats.setGeometry(QtCore.QRect(1050, 690, 361, 201))
        self.Dcache_stats.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Dcache_stats.setReadOnly(True)
        self.Dcache_stats.setFont(font)
        self.Dcache_stats.setObjectName("Dcache_stats")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        self.assemble_button.clicked.connect(self.assemble)
        self.run_button.clicked.connect(self.run)
        self.step_button.clicked.connect(self.step)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RISC-V Simulator"))
        self.assemble_button.setText(_translate("MainWindow", "Assemble"))
        self.step_button.setText(_translate("MainWindow", "Step"))
        self.run_button.setText(_translate("MainWindow", "Run"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600; text-decoration: underline;\">Machine code</span></p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Clock</span></p></body></html>"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600; text-decoration: underline;\">Console</span></p></body></html>"))
        self.pipe_forward_radio.setText(_translate("MainWindow", "Pipelined with forwarding"))
        self.pipe_no_forward_radio.setText(_translate("MainWindow", "Pipelined, no-forwarding"))
        self.no_pipe_radio.setText(_translate("MainWindow", "Non-pipelined"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600; text-decoration: underline;\">Register File</span></p></body></html>"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), _translate("MainWindow", "Register"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600; text-decoration: underline;\">Main Memory</span></p></body></html>"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), _translate("MainWindow", "Memory"))
        self.label_8.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">I$</span></p></body></html>"))
        self.label_10.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">Cache size:</span></p></body></html>"))
        self.label_11.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">D$</span></p></body></html>"))
        self.label_13.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">Block size:</span></p></body></html>"))
        self.label_14.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">Associativity:</span></p></body></html>"))
        self.label_12.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">Cache size:</span></p></body></html>"))
        self.label_15.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">Block size:</span></p></body></html>"))
        self.label_16.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">Associativity:</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Code"))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600; text-decoration: underline;\">I$</span></p></body></html>"))
        self.label_7.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600; text-decoration: underline;\">D$</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Cache"))

    def update_inst_cache(self, dic, block_size):
        self.Icache_output.setRowCount(0)
        self.Icache_output.setColumnCount(block_size+1)
        self.Icache_output.setColumnWidth(0, 120)
        for i in range(block_size):
            self.Icache_output.setColumnWidth(i+1, 54)
        #self.tableWidget2.setColumnWidth(2, 150)

        self.Icache_output.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("Tag"))
        for i in range(block_size):
            self.Icache_output.setHorizontalHeaderItem(i+1, QtWidgets.QTableWidgetItem(f"+{i}"))
        #self.tableWidget2.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem("Contents"))

        for key, value in dic.items():
            self.Icache_output.insertRow(self.Icache_output.rowCount())
            self.Icache_output.setItem(self.Icache_output.rowCount()-1, 0,QtWidgets.QTableWidgetItem(self.padhexa(hex(key)).upper().replace('X', 'x')))
            s = [i for i in value]
            for i, val in enumerate(s):
                self.Icache_output.setItem(self.Icache_output.rowCount()-1, i+1,QtWidgets.QTableWidgetItem(self.padhexa(hex(val),2).upper().replace('X', 'x')))

    def update_data_cache(self, dic, block_size):
        self.Dcache_output.setRowCount(0)
        self.Dcache_output.setColumnCount(block_size+1)
        self.Dcache_output.setColumnWidth(0, 120)
        for i in range(block_size):
            self.Dcache_output.setColumnWidth(i+1, 54)
        

        self.Dcache_output.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("Tag"))
        for i in range(block_size):
            self.Dcache_output.setHorizontalHeaderItem(i+1, QtWidgets.QTableWidgetItem(f"+{i}"))

        for key, value in dic.items():
            self.Dcache_output.insertRow(self.Dcache_output.rowCount())
            self.Dcache_output.setItem(self.Dcache_output.rowCount()-1, 0,QtWidgets.QTableWidgetItem((self.padhexa(hex(key)).upper().replace('X', 'x'))))
            s = [i for i in value]
            for i, val in enumerate(s):
                self.Dcache_output.setItem(self.Dcache_output.rowCount()-1, i+1,QtWidgets.QTableWidgetItem(self.padhexa(hex(val),2).upper().replace('X', 'x')))

    def reload_modules(self):
        importlib.reload(RunSim_forward)
        importlib.reload(RunSim_stall)
        importlib.reload(RunSim_non_pipelined)
        importlib.reload(MachineCodeParser)
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
        global error
        error=False
        try:
            inst_cache_size=int(self.Icache_size.text())
            inst_cache_block_size=int(self.Icache_blocksize.text())
            inst_cache_associativity=int(self.Icache_assoc.text())
            data_cache_size=int(self.Dcache_size.text())
            data_cache_block_size=int(self.Dcache_blocksize.text())
            data_cache_associativity=int(self.Dcache_assoc.text())  
        except:
            self.console.setPlainText("Invalid Cache Specifications!")
            error=True
            return
        self.console.clear()
        if inst_cache_size < inst_cache_block_size:
            self.console.appendPlainText("I$: Invalid selection of cache block size and cache size!")
            error=True
        if inst_cache_block_size < 4 or math.log(inst_cache_block_size, 2) != int(math.log(inst_cache_block_size, 2)):
            self.console.appendPlainText("I$: Cache block size must be a power of 2 and >=4 bytes!")
            error=True
        if inst_cache_size < 4 or math.log(inst_cache_size, 2) != int(math.log(inst_cache_size, 2)):
            self.console.appendPlainText("I$: Cache size must be a power of 2 and >=4 bytes!")
            error=True
        if math.log(inst_cache_associativity, 2) != int(math.log(inst_cache_associativity, 2)) or inst_cache_associativity > inst_cache_size // inst_cache_block_size:
            self.console.appendPlainText("I$: Associativity must be a power of 2 and less than total number of blocks!")
            error=True

        if data_cache_size < data_cache_block_size:
            self.console.appendPlainText("D$: Invalid selection of cache block size and cache size!")
            error=True
        if data_cache_block_size < 4 or math.log(data_cache_block_size, 2) != int(math.log(data_cache_block_size, 2)):
            self.console.appendPlainText("D$: Cache block size must be a power of 2 and >=4 bytes!")
            error=True
        if data_cache_size < 4 or math.log(data_cache_size, 2) != int(math.log(data_cache_size, 2)):
            self.console.appendPlainText("D$: Cache size must be a power of 2 and >=4 bytes!")
            error=True
        if math.log(data_cache_associativity, 2) != int(math.log(data_cache_associativity, 2)) or data_cache_associativity > data_cache_size // data_cache_block_size:
            self.console.appendPlainText("D$: Associativity must be a power of 2 and less than total number of blocks!")
            error=True
        if error:
            return

        self.reload_modules()
        global finished
        finished=False
        code = self.MachineCodeInput.toPlainText()
        fhand = open("gui_instructions.mc", "w")
        fhand.write(code)
        fhand.close()
        MachineCodeParser.parser("gui_instructions.mc")
        RunSim_forward.memory.InitMemory(MachineCodeParser.PC_INST, MachineCodeParser.DATA, inst_cache_size, inst_cache_block_size, inst_cache_associativity, data_cache_size, data_cache_block_size, data_cache_associativity)
        RunSim_stall.memory.InitMemory(MachineCodeParser.PC_INST, MachineCodeParser.DATA, inst_cache_size, inst_cache_block_size, inst_cache_associativity, data_cache_size, data_cache_block_size, data_cache_associativity)
        RunSim_non_pipelined.memory.InitMemory(MachineCodeParser.PC_INST, MachineCodeParser.DATA, inst_cache_size, inst_cache_block_size, inst_cache_associativity, data_cache_size, data_cache_block_size, data_cache_associativity)
        print("\033[92mProgram and data loaded to memory successfully\033[0m")
        self.console.setPlainText("Program and data loaded to memory successfully!")
        self.clock_display.display(0)
        self.Icache_output.clear()
        self.Dcache_output.clear()
        self.Icache_output.setRowCount(0)
        self.Icache_output.setColumnCount(0)
        self.Dcache_output.setColumnCount(0)
        self.Dcache_output.setRowCount(0)
        self.Icache_stats.clear()
        self.Dcache_stats.clear()
        self.MemoryOutput.clear()
        self.MemoryOutput.setRowCount(0)
        self.MemoryOutput.setColumnCount(0)
        self.RegisterOutput.clear()
        # self.RegisterOutput.setRowCount(0)
        # self.RegisterOutput.setColumnCount(0)

    def padhexa(self, s, pres=8):
        return '0x' + s[2:].zfill(pres)

    def update_registers(self, arr):
        self.RegisterOutput.setRowCount(0)
        self.RegisterOutput.setColumnCount(2)
        self.RegisterOutput.setColumnWidth(0, 15)
        self.RegisterOutput.setColumnWidth(1, 200)
        self.RegisterOutput.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("Reg"))
        self.RegisterOutput.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("Value"))
        for i in range(32):
            text = "x" + str(i)
            self.RegisterOutput.insertRow(self.RegisterOutput.rowCount())
            self.RegisterOutput.setItem(self.RegisterOutput.rowCount() - 1, 0,
                                     QtWidgets.QTableWidgetItem(text.upper()))
            # print address of register for eg. x5
            if arr[i] >= 0:
                self.RegisterOutput.setItem(self.RegisterOutput.rowCount() - 1, 1,
                                         QtWidgets.QTableWidgetItem((self.padhexa(hex(arr[i]))).upper().replace('X', 'x')))

            else:
                reg = arr[i] & 0xffffffff  # signed
                self.RegisterOutput.setItem(self.RegisterOutput.rowCount() - 1, 1,
                                         QtWidgets.QTableWidgetItem((hex(reg)).upper().replace('X', 'x')))

    def update_memory(self, dic):
        lst = []  # stores keys present in dictionary
        temp_lst = []  # stores base address
        self.MemoryOutput.setRowCount(0)
        self.MemoryOutput.setColumnCount(5)
        self.MemoryOutput.setColumnWidth(0, 130)
        self.MemoryOutput.setColumnWidth(1, 10)
        self.MemoryOutput.setColumnWidth(2, 10)
        self.MemoryOutput.setColumnWidth(3, 10)
        self.MemoryOutput.setColumnWidth(4, 10)
        self.MemoryOutput.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("Address"))
        self.MemoryOutput.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("+0"))
        self.MemoryOutput.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem("+1"))
        self.MemoryOutput.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem("+2"))
        self.MemoryOutput.setHorizontalHeaderItem(4, QtWidgets.QTableWidgetItem("+3"))
        for key in dic:
            lst.append(key)
        lst.sort()
        for x in lst:
            temp = x - (x % 4)  # storing base address in temp
            if temp not in temp_lst:  # if base address not present in temp_list , then append it
                temp_lst.append(temp)
        temp_lst.sort()
        for i in temp_lst:
            self.MemoryOutput.insertRow(self.MemoryOutput.rowCount())
            self.MemoryOutput.setItem(self.MemoryOutput.rowCount() - 1, 0,
                                     QtWidgets.QTableWidgetItem((self.padhexa(hex(i)).upper().replace('X', 'x'))))
            if i in lst:
                self.MemoryOutput.setItem(self.MemoryOutput.rowCount() - 1, 1,
                                         QtWidgets.QTableWidgetItem((self.padhexa(hex(dic[i])).upper())[8:]))
            else:
                self.MemoryOutput.setItem(self.MemoryOutput.rowCount() - 1, 1, QtWidgets.QTableWidgetItem("00"))
            if (i + 1) in lst:

                self.MemoryOutput.setItem(self.MemoryOutput.rowCount() - 1, 2,
                                         QtWidgets.QTableWidgetItem((self.padhexa(hex(dic[i + 1])).upper())[8:]))
            else:

                self.MemoryOutput.setItem(self.MemoryOutput.rowCount() - 1, 2, QtWidgets.QTableWidgetItem("00"))
            if (i + 2) in lst:

                self.MemoryOutput.setItem(self.MemoryOutput.rowCount() - 1, 3,
                                         QtWidgets.QTableWidgetItem((self.padhexa(hex(dic[i + 2])).upper())[8:]))
            else:

                self.MemoryOutput.setItem(self.MemoryOutput.rowCount() - 1, 3, QtWidgets.QTableWidgetItem("00"))
            if (i + 3) in lst:

                self.MemoryOutput.setItem(self.MemoryOutput.rowCount() - 1, 4,
                                         QtWidgets.QTableWidgetItem((self.padhexa(hex(dic[i + 3])).upper())[8:]))
            else:

                self.MemoryOutput.setItem(self.MemoryOutput.rowCount() - 1, 4, QtWidgets.QTableWidgetItem("00"))

    def run(self):
        global error
        global finished
        if error or finished:
            return
        reg_list=[]
        mem_dict={}
        stats=None
        if pipeline==0:
            stats=RunSim_non_pipelined.RunSim(1,1)
            mem_dict= {**RunSim_non_pipelined.memory.text_module.memory, **RunSim_non_pipelined.memory.data_module.memory}#RunSim_non_pipelined.memory.text_module.update(RunSim_non_pipelined.memory.data_module)
            reg_list=RunSim_non_pipelined.registers.reg
            self.update_memory(mem_dict)
            self.update_registers(reg_list)
            self.update_inst_cache(RunSim_non_pipelined.memory.text_module.cache_module.cache_dict, RunSim_non_pipelined.memory.text_module.cache_block_size)
            self.update_data_cache(RunSim_non_pipelined.memory.data_module.cache_module.cache_dict, RunSim_non_pipelined.memory.data_module.cache_block_size)
            self.Icache_stats.setPlainText(f"Total Accesses: {RunSim_non_pipelined.memory.text_module.cache_accesses}\n\nTotal Hits: {RunSim_non_pipelined.memory.text_module.cache_hits}\n\nTotal Miss: {RunSim_non_pipelined.memory.text_module.cache_miss}")
            self.Dcache_stats.setPlainText(f"Total Accesses: {RunSim_non_pipelined.memory.data_module.cache_accesses}\n\nTotal Hits: {RunSim_non_pipelined.memory.data_module.cache_hits}\n\nTotal Miss: {RunSim_non_pipelined.memory.data_module.cache_miss}")
            self.clock_display.display(RunSim_non_pipelined.clock)
        if pipeline==1:
            stats=RunSim_stall.RunSim(1,1)
            mem_dict={**RunSim_stall.memory.text_module.memory, **RunSim_stall.memory.data_module.memory}
            self.update_memory(mem_dict)
            self.update_inst_cache(RunSim_stall.memory.text_module.cache_module.cache_dict, RunSim_stall.memory.text_module.cache_block_size)
            self.update_data_cache(RunSim_stall.memory.data_module.cache_module.cache_dict, RunSim_stall.memory.data_module.cache_block_size)
            reg_list=RunSim_stall.registers.reg
            self.update_registers(reg_list)
            self.Icache_stats.setPlainText(f"Total Accesses: {RunSim_stall.memory.text_module.cache_accesses}\n\nTotal Hits: {RunSim_stall.memory.text_module.cache_hits}\n\nTotal Miss: {RunSim_stall.memory.text_module.cache_miss}")
            self.Dcache_stats.setPlainText(f"Total Accesses: {RunSim_stall.memory.data_module.cache_accesses}\n\nTotal Hits: {RunSim_stall.memory.data_module.cache_hits}\n\nTotal Miss: {RunSim_stall.memory.data_module.cache_miss}")
            self.clock_display.display(RunSim_stall.clock)
        if pipeline==2:
            stats=RunSim_forward.RunSim(1,1)
            mem_dict={**RunSim_forward.memory.text_module.memory, **RunSim_forward.memory.data_module.memory}
            self.update_memory(mem_dict)
            self.update_inst_cache(RunSim_forward.memory.text_module.cache_module.cache_dict, RunSim_forward.memory.text_module.cache_block_size)
            self.update_data_cache(RunSim_forward.memory.data_module.cache_module.cache_dict, RunSim_forward.memory.data_module.cache_block_size)
            reg_list=RunSim_forward.registers.reg
            self.update_registers(reg_list)
            self.Icache_stats.setPlainText(f"Total Accesses: {RunSim_forward.memory.text_module.cache_accesses}\n\nTotal Hits: {RunSim_forward.memory.text_module.cache_hits}\n\nTotal Miss: {RunSim_forward.memory.text_module.cache_miss}")
            self.Dcache_stats.setPlainText(f"Total Accesses: {RunSim_forward.memory.data_module.cache_accesses}\n\nTotal Hits: {RunSim_forward.memory.data_module.cache_hits}\n\nTotal Miss: {RunSim_forward.memory.data_module.cache_miss}")
            self.clock_display.display(RunSim_forward.clock)
        with open(f"RegisterDump.mc", "w") as fileReg:
            for i in range(32): # for all 32 registers
                fileReg.write(f"x{i} ")  # print address of register for eg. x5
                if (reg_list[i] >= 0):
                    fileReg.write(self.padhexa(hex(reg_list[i])).upper().replace('X', 'x'))
                else:
                    reg = reg_list[i] & 0xffffffff  # signed
                    fileReg.write(hex(reg).upper().replace('X', 'x'))
                fileReg.write("\n")

        #dumping memory
        with open(f"MemoryDump.mc", "w") as fileMem:  # input is dictionary with key as address and value as data
            lst = []  # stores keys present in dictionary
            temp_lst = []  # stores base mem_dict:
            for key in mem_dict:
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
                    fileMem.write(f"{(self.padhexa(hex(mem_dict[i])).upper())[8:]} " )  # if key in dictionary, print its data
                else:
                    fileMem.write("00 ")  # if key not in dictionary, print 00
                if (i + 1) in lst:
                    fileMem.write(f"{(self.padhexa(hex(mem_dict[i + 1])).upper())[8:]} ")
                else:
                    fileMem.write("00 ")
                if (i + 2) in lst:
                    fileMem.write(f"{(self.padhexa(hex(mem_dict[i + 2])).upper())[8:]} ")
                else:
                    fileMem.write("00 ")
                if (i + 3) in lst:
                    fileMem.write(f"{(self.padhexa(hex(mem_dict[i + 3])).upper())[8:]} ")
                else:
                    fileMem.write("00  ")
                fileMem.write("\n")  # new line
        
        print("\033[1;92mRegister and memory outputs written in RegisterDump.mc and MemoryDump.mc respectively\033[0m")
        if stats=="NPE": # for non pipelined ending
            self.console.setPlainText("Program Terminated Successfully!")
            finished=True
        elif stats!=None:
            self.console.setPlainText("Program Terminated Successfully!")
            self.console.appendPlainText("Stats-")
            self.console.appendPlainText(f"Stat1: Cycles: {stats[0]}")
            self.console.appendPlainText(f"Stat2: Total Instructions: {stats[1]}")
            self.console.appendPlainText(f"Stat3: CPI: {stats[2]}")
            self.console.appendPlainText(f"Stat4: Load/Store: {stats[3]}")
            self.console.appendPlainText(f"Stat5: ALU instructions: {stats[4]}")
            self.console.appendPlainText(f"Stat6: Control instructions: {stats[5]}")
            self.console.appendPlainText(f"Stat7: Bubbles: {stats[6]}")
            self.console.appendPlainText(f"Stat8: Total Data Hazards: {stats[7]}")
            self.console.appendPlainText(f"Stat9: Total Control Hazards: {stats[8]}")
            self.console.appendPlainText(f"Stat10: Total branch mispredictions: {stats[9]}")
            self.console.appendPlainText(f"Stat11: Stalls due to data hazard: {stats[10]}")
            self.console.appendPlainText(f"Stat12: Stalls due to control hazard: {stats[11]}")
            finished=True
            self.console.verticalScrollBar().setValue(0)


    def step(self):
        global error
        global finished
        if error or finished:
            return
        reg_list=[]
        mem_dict={}
        stats=None
        if pipeline==0:
            stats=RunSim_non_pipelined.RunSim_step(1,1)
            mem_dict= {**RunSim_non_pipelined.memory.text_module.memory, **RunSim_non_pipelined.memory.data_module.memory}#RunSim_non_pipelined.memory.text_module.update(RunSim_non_pipelined.memory.data_module)
            self.update_memory(mem_dict)
            self.update_inst_cache(RunSim_non_pipelined.memory.text_module.cache_module.cache_dict, RunSim_non_pipelined.memory.text_module.cache_block_size)
            self.update_data_cache(RunSim_non_pipelined.memory.data_module.cache_module.cache_dict, RunSim_non_pipelined.memory.data_module.cache_block_size)
            reg_list=RunSim_non_pipelined.registers.reg
            self.update_registers(reg_list)
            self.Icache_stats.setPlainText(f"Total Accesses: {RunSim_non_pipelined.memory.text_module.cache_accesses}\n\nTotal Hits: {RunSim_non_pipelined.memory.text_module.cache_hits}\n\nTotal Miss: {RunSim_non_pipelined.memory.text_module.cache_miss}")
            self.Dcache_stats.setPlainText(f"Total Accesses: {RunSim_non_pipelined.memory.data_module.cache_accesses}\n\nTotal Hits: {RunSim_non_pipelined.memory.data_module.cache_hits}\n\nTotal Miss: {RunSim_non_pipelined.memory.data_module.cache_miss}")
            self.clock_display.display(RunSim_non_pipelined.clock)
        if pipeline==1:
            stats=RunSim_stall.RunSim_step(1,1)
            mem_dict={**RunSim_stall.memory.text_module.memory, **RunSim_stall.memory.data_module.memory}
            self.update_memory(mem_dict)
            self.update_inst_cache(RunSim_stall.memory.text_module.cache_module.cache_dict, RunSim_stall.memory.text_module.cache_block_size)
            self.update_data_cache(RunSim_stall.memory.data_module.cache_module.cache_dict, RunSim_stall.memory.data_module.cache_block_size)
            reg_list=RunSim_stall.registers.reg
            self.update_registers(reg_list)
            self.Icache_stats.setPlainText(f"Total Accesses: {RunSim_stall.memory.text_module.cache_accesses}\n\nTotal Hits: {RunSim_stall.memory.text_module.cache_hits}\n\nTotal Miss: {RunSim_stall.memory.text_module.cache_miss}")
            self.Dcache_stats.setPlainText(f"Total Accesses: {RunSim_stall.memory.data_module.cache_accesses}\n\nTotal Hits: {RunSim_stall.memory.data_module.cache_hits}\n\nTotal Miss: {RunSim_stall.memory.data_module.cache_miss}")
            self.clock_display.display(RunSim_stall.clock)
        if pipeline==2:
            stats=RunSim_forward.RunSim_step(1,1)
            mem_dict={**RunSim_forward.memory.text_module.memory, **RunSim_forward.memory.data_module.memory}
            self.update_memory(mem_dict)
            self.update_inst_cache(RunSim_forward.memory.text_module.cache_module.cache_dict, RunSim_forward.memory.text_module.cache_block_size)
            self.update_data_cache(RunSim_forward.memory.data_module.cache_module.cache_dict, RunSim_forward.memory.data_module.cache_block_size)
            reg_list=RunSim_forward.registers.reg
            self.update_registers(reg_list)
            self.Icache_stats.setPlainText(f"Total Accesses: {RunSim_forward.memory.text_module.cache_accesses}\n\nTotal Hits: {RunSim_forward.memory.text_module.cache_hits}\n\nTotal Miss: {RunSim_forward.memory.text_module.cache_miss}")
            self.Dcache_stats.setPlainText(f"Total Accesses: {RunSim_forward.memory.data_module.cache_accesses}\n\nTotal Hits: {RunSim_forward.memory.data_module.cache_hits}\n\nTotal Miss: {RunSim_forward.memory.data_module.cache_miss}")
            self.clock_display.display(RunSim_forward.clock)
        with open(f"RegisterDump.mc", "w") as fileReg:
            for i in range(32): # for all 32 registers
                fileReg.write(f"x{i} ")  # print address of register for eg. x5
                if (reg_list[i] >= 0):
                    fileReg.write(self.padhexa(hex(reg_list[i])).upper().replace('X', 'x'))
                else:
                    reg = reg_list[i] & 0xffffffff  # signed
                    fileReg.write(hex(reg).upper().replace('X', 'x'))
                fileReg.write("\n")

        #dumping memory
        with open(f"MemoryDump.mc", "w") as fileMem:  # input is dictionary with key as address and value as data
            lst = []  # stores keys present in dictionary
            temp_lst = []  # stores base mem_dict:
            for key in mem_dict:
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
                    fileMem.write(f"{(self.padhexa(hex(mem_dict[i])).upper())[8:]} " )  # if key in dictionary, print its data
                else:
                    fileMem.write("00 ")  # if key not in dictionary, print 00
                if (i + 1) in lst:
                    fileMem.write(f"{(self.padhexa(hex(mem_dict[i + 1])).upper())[8:]} ")
                else:
                    fileMem.write("00 ")
                if (i + 2) in lst:
                    fileMem.write(f"{(self.padhexa(hex(mem_dict[i + 2])).upper())[8:]} ")
                else:
                    fileMem.write("00 ")
                if (i + 3) in lst:
                    fileMem.write(f"{(self.padhexa(hex(mem_dict[i + 3])).upper())[8:]} ")
                else:
                    fileMem.write("00  ")
                fileMem.write("\n")  # new line
        if stats=="NPE": # for non pipelined ending
            self.console.setPlainText("Program Terminated Successfully!")
            finished=True
        elif stats!=None:
            self.console.setPlainText("Program Terminated Successfully!")
            self.console.appendPlainText("Stats-")
            self.console.appendPlainText(f"Stat1: Cycles: {stats[0]}")
            self.console.appendPlainText(f"Stat2: Total Instructions: {stats[1]}")
            self.console.appendPlainText(f"Stat3: CPI: {stats[2]}")
            self.console.appendPlainText(f"Stat4: Load/Store: {stats[3]}")
            self.console.appendPlainText(f"Stat5: ALU instructions: {stats[4]}")
            self.console.appendPlainText(f"Stat6: Control instructions: {stats[5]}")
            self.console.appendPlainText(f"Stat7: Bubbles: {stats[6]}")
            self.console.appendPlainText(f"Stat8: Total Data Hazards: {stats[7]}")
            self.console.appendPlainText(f"Stat9: Total Control Hazards: {stats[8]}")
            self.console.appendPlainText(f"Stat10: Total branch mispredictions: {stats[9]}")
            self.console.appendPlainText(f"Stat11: Stalls due to data hazard: {stats[10]}")
            self.console.appendPlainText(f"Stat12: Stalls due to control hazard: {stats[11]}")
            finished=True
            self.console.verticalScrollBar().setValue(0)
            print("\033[1;92mRegister and memory outputs written in RegisterDump.mc and MemoryDump.mc respectively\033[0m")
        else:
            self.console.setPlainText("Executing....")

# if __name__ == "__main__":
import sys
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
MainWindow.setGeometry(225,60,1436, 944)
MainWindow.setFixedSize(1436, 944)
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
