# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
import sys, os
import numpy as np
import socket
import cv2
import binascii
import PyQt5.sip
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow

a = 0
ll = 0
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 619)
        MainWindow.setMinimumSize(QtCore.QSize(320, 240))
        MainWindow.setMaximumSize(QtCore.QSize(1920, 1080))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 800, 600))
        self.label.setText("")
        self.label.setObjectName("label")
        self.openbutton = QtWidgets.QPushButton(self.centralwidget)
        self.openbutton.setGeometry(QtCore.QRect(820, 240, 200, 50))
        self.openbutton.setObjectName("openbutton")
        self.closebutton = QtWidgets.QPushButton(self.centralwidget)
        self.closebutton.setGeometry(QtCore.QRect(820, 300, 200, 50))
        self.closebutton.setObjectName("closebutton")
        self.warnbutton = QtWidgets.QPushButton(self.centralwidget)
        self.warnbutton.setGeometry(QtCore.QRect(820, 360, 200, 50))
        self.warnbutton.setObjectName("closebutton_2")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(940, 10, 81, 31))
        self.textEdit.setObjectName("textEdit")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(850, 10, 81, 31))
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(False)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(860, 100, 150, 31))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
#        self.label_4 = QtWidgets.QLabel(self.centralwidget)
#        s#elf.label_4.setGeometry(QtCore.QRect(860, 150, 131, 31))
#        self.label_4.setText("")
#        self.label_4.setObjectName("label_4")
        self.connectButton = QtWidgets.QPushButton(self.centralwidget)
        self.connectButton.setGeometry(QtCore.QRect(860, 50, 161, 41))
        self.connectButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.openbutton.setText(_translate("MainWindow", "打开图像"))
        self.closebutton.setText(_translate("MainWindow", "关闭图像"))
        self.warnbutton.setText(_translate("MainWindow", "报警"))
        self.label_2.setText(_translate("MainWindow", "端口号："))
        self.connectButton.setText(_translate("MainWindow", "连接"))

    def connect(self):

        global a
        global s
        if a == 0:
            a = 1
            com = ui.textEdit.toPlainText()
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            s.close()
            print('本机：' + ip)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind((ip, int(com)))
            print('connected')
            ui.connectButton.setText("断开连接")
            ui.label_3.setText('本机IP:' + ip)
#            s.sendto(('aaa').encode('utf-8'), ('127.0.0.1', 777))
        else :
            a = 0
            s.close()
            print('close')
            ui.connectButton.setText("连接")

    def slotStart(self):
        if a == 1:
            self.timer_camera.start(50)
            self.timer_camera.timeout.connect(self.openFrame)
            ui.connectButton.setEnabled(False)


    def slotStop(self):
        self.timer_camera.stop()   # 停止计时器
        ui.warnbutton.setEnabled(False)
        ui.connectButton.setEnabled(True)

    def openFrame(self):
        global  addr
        ui.warnbutton.setEnabled(True)
        list = []
        buf, addr = s.recvfrom(4096)
        bufx1 = binascii.b2a_hex(buf).decode('utf-8')
        if bufx1[0:4] == 'ffd8' and bufx1[(len(bufx1) - 4):len(bufx1)] != 'ffd9':    #数据包包头
            list.append(buf)
            buf, addr = s.recvfrom(4096)
            bufx1 = binascii.b2a_hex(buf).decode('utf-8')
            while bufx1[(len(bufx1) - 4):len(bufx1)] != 'ffd9':    #数据包包尾
                list.append(buf)
                buf, addr = s.recvfrom(4096)
                bufx1 = binascii.b2a_hex(buf).decode('utf-8')
            buff = b''.join(list)
            nparr = np.fromstring(buff, np.uint8)     #解码
            img_decode = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#            cv2.imshow('result', img_decode)   #打开opencv的小窗口
#            cv2.waitKey(1)
            frame = cv2.cvtColor(img_decode, cv2.COLOR_BGR2RGB)
            height, width, bytesPerComponent = frame.shape
            bytesPerLine = bytesPerComponent * width
            q_image = QImage(frame.data,  width, height, bytesPerLine,
            QImage.Format_RGB888).scaled(self.label.width(), self.label.height())
            ui.label.setPixmap(QPixmap.fromImage(q_image))
#            ui.label_4.setText('摄像头IP：' + addr)
        else:
            self.timer_camera.stop()

    def led(self):
        global ll
        if ll == 0:
            ll = 1
            s.sendto(('1').encode('utf-8'), addr)
        else:
            ll = 0
            s.sendto(('0').encode('utf-8'), addr)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.timer_camera = QTimer()  # 定义定时器
    ui.openbutton.clicked.connect(ui.slotStart)  # 按钮关联槽函数
    ui.closebutton.clicked.connect(ui.slotStop)
    ui.connectButton.clicked.connect(ui.connect)
    ui.warnbutton.clicked.connect(ui.led)
    ui.warnbutton.setEnabled(False)
    sys.exit(app.exec_())