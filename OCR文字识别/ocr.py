import sys, os
import PyQt5.sip
from aip import AipOcr
import time
# from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog, QTextEdit
from PyQt5.QtGui import *
# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtCore import QCoreApplication
from ui import Ui_MainWindow
import cv2 as cv
flag = 0
# """ 你的 APPID AK SK """
APP_ID = '19204529'
API_KEY = 'QQhn3CMhKDXso283KpSXlPKx'
SECRET_KEY = 'QB1D6ynyMQoudfQV0CCGg6YC9sGIQdTS'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def showDialog():
    global img
    close_image()
    fname = QFileDialog.getOpenFileName(caption='Open File', filter='*.jpg;;*.png;;All Files(*)')
    img = fname[0]
    ui.label.setPixmap(QPixmap(img).scaled(ui.label.width(), ui.label.height()))
#    ui.label.setPixmap(QPixmap(img).re)
    print(img)


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def ocr(self):

    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "true"
    ui.openButton.setEnabled(True)
#    print(img)
    if flag == 0:
        with open(str(img), 'rb') as fp:
            image = fp.read()
    else:
        with open('123.jpg', 'rb') as fp:
            image = fp.read()
        flag == 0
    time.sleep(0.5)
    result = client.basicGeneral(image, options)
    count = result['words_result_num']
    if count > 0:
        ui.label_2.setText('识别成功')
    else:
        ui.label_2.setText('识别失败')
#    print(count)
    for a in range(0, count):
#        print(result['words_result'][a]['words'])
        ui.plainTextEdit.insertPlainText(result['words_result'][a]['words']+'\n')
#        ui.plainTextEdit.insertPlainText('\n')

def save_txt():
    txt_name = QFileDialog.getSaveFileName(caption='Save File', filter='*.txt;;All Files(*)')
    time.sleep(0.5)
    print(txt_name[0])
    if txt_name[0]:
        with open(txt_name[0], "w") as f:
            txt_image = ui.plainTextEdit.toPlainText()
#            f.flush()
            f.write(txt_image)
            print(txt_image)
            f.close()


def close_image():
    global flag
    ui.label.setText('image')
    ui.plainTextEdit.setPlainText('')
    ui.openButton.setEnabled(True)
    ui.label_2.setText('')
    flag = 0

def open_cam():
    global cap
    global re
    close_image()
    cap = cv.VideoCapture(0)
    ui.closecamButton.setEnabled(True)
    ui.camButton.setEnabled(False)
    ui.openButton.setEnabled(False)
    while cap.isOpened():
        ret, src = cap.read()
        asd = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
        re = cv.resize(asd, (320, 240))
        cv.imshow('2222', re)
        cv.waitKey(30)

def close_cam():

    time.sleep(0.5)
    ui.closecamButton.setEnabled(False)
    ui.camButton.setEnabled(True)
    ui.openButton.setEnabled(True)
#    ui.label.setText('image')
    cap.release()
    cv.destroyAllWindows()

def load_image():
    global flag
    flag = 1
    cv.imwrite('123.jpg', re)
    time.sleep(0.5)
    ui.label.setPixmap(QPixmap('123.jpg').scaled(ui.label.width(), ui.label.height()))
    ui.openButton.setEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.closeButton.clicked.connect(close_image)
    ui.openButton.clicked.connect(showDialog)
    ui.shibieButton.clicked.connect(ocr)
    ui.saveButton.clicked.connect(save_txt)
    ui.camButton.clicked.connect(open_cam)
    ui.closecamButton.clicked.connect(close_cam)
    ui.loadButton.clicked.connect(load_image)
    sys.exit(app.exec_())

