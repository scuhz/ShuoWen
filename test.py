# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QBasicTimer,Qt
from PyQt5.QtGui import QPalette
from subprocess import Popen, PIPE, STDOUT
import os
from docx import  Document
import time

class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 519)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 170, 71, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(170, 50, 41, 16))
        self.label_2.setObjectName("label_2")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(210, 50, 118, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.timer = QBasicTimer()
        self.step = 0
        self.analysis_time = 0
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(140, 80, 211, 251))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 209, 249))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.inputButton = QtWidgets.QPushButton(self.centralwidget)
        self.inputButton.setGeometry(QtCore.QRect(40, 210, 56, 17))
        self.inputButton.setObjectName("inputButton")
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(140, 340, 56, 17))
        self.saveButton.setObjectName("saveButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 404, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.inputButton.clicked.connect(self.handle_click)
        self.saveButton.clicked.connect(self.save_click)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "请上传您的文件"))
        self.label_2.setText(_translate("MainWindow", "正在分析"))
        self.inputButton.setText(_translate("MainWindow", "上传文件"))
        MainWindow.setWindowOpacity(0.9)
        #MainWindow.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        pe=QPalette()
        MainWindow.setAutoFillBackground(True)
        pe.setColor(QPalette.Window,Qt.lightGray)
        MainWindow.setPalette(pe)


    def timerEvent(self, e):
        if self.step >= self.analysis_time:
            self.timer.stop()
            self.label_2.setText('分析完成')
            return
        self.step = self.step + self.analysis_time/100
        print(self.step)
        self.progressBar.setValue(self.step)

    def handle_click(self):
        print("hello")
        file_path, filetype = QFileDialog.getOpenFileName(self,
                                                          "选取文件",
                                                          "./",
                                                          "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,注意用双分号间隔
        print(file_path, filetype)
        file_path_str = str(file_path)
        time_start = time.time()
        time.sleep(5)
        time_end =time.time()
        self.analysis_time = time_end-time_start
        print(self.analysis_time)
        self.progressBar.setMaximum(self.analysis_time)
        self.timer.start(100, self)
        '''
        bat_path=os.path.join(os.getcwd(),"kk.bat")
        time_start = time.time()
        cmd = "cmd.exe "+bat_path+" "+file_path_str
        print(cmd)
        result = Popen(cmd,stdout=PIPE,stderr=STDOUT)
        time_end =time.time()
        self.analysis_time = time_end-time_start
        self.progressBar.setMaximum(self.analysis_time)
        self.timer.start(100, self)#时间间隔为100ms
        print(result)
        doc = Document(result)
        '''


    def save_click(self):
        file_save_path, ok2 = QFileDialog.getSaveFileName(self,
                                                     "文件保存",
                                                     "./",
                                                     "All Files (*);;Text Files (*.txt)")
        print(file_save_path)
        # doc.save(file_save_path) #'保存doc文件到路径file_save_path'
if __name__=='__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
