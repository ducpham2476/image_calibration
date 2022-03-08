from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog, QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QPixmap
import sys
import os
import cv2
import threading


parent = os.getcwd()

reference_filename = "./images/camera-capture-dummy.jpg"

class define_parking_lot(QMainWindow):
    global reference_filename

    image_show_flag = False

    def __init__(self):
        print(reference_filename)

        super(define_parking_lot, self).__init__()
        uic.loadUi('define-parking-lot.ui', self)

        # print("Define parking lot: {}".format(reference_filename))
        # # if reference_filename == "":
        # #     pass
        # # else:
        # print("Run this line")
        # input_image = cv2.imread(reference_filename)
        # resized_image = cv2.resize(input_image, (960, 540))
        # height, width, bytesPerComponent = resized_image.shape
        # bytesPerLine = 3 * width
        # cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB, resized_image)
        # # cv2.imshow("Image", resized_image)
        # # cv2.waitKey()
        #
        # q_image = QtGui.QImage(resized_image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        #
        # pixmap = QtGui.QPixmap.fromImage(q_image)
        # self.image_editor.setPixmap(pixmap)
        #
        # self.image_editor.setCursor(QtCore.Qt.CrossCursor)
        self.image_editor = image_painter(self.image_disp)

        # self.back_B.clicked.connect(self.select_reference_image)
        # self.load_B.clicked.connect(self.load_image)
        self.load_image()

        self.show() # Show the GUI

    def load_image(self):

        # self.image_editor = image_painter(self.image_disp)
        #print("Define parking lot: {}".format(reference_filename))

        reload_menu = threading.Timer(2.0, self.load_image)
        reload_menu.start()

        # if reference_filename == "":
        #     pass
        # else:
        if reference_filename == "":
            print("pass")
            pass
        else:
            input_image = cv2.imread(reference_filename)
            # cv2.imshow("Input image", input_image)
            # cv2.waitKey(1)
            resized_image = cv2.resize(input_image, (960, 540))
            # print(self.image_disp.width(), self.image_disp.height())

            # cv2.imshow("Resized image", resized_image)
            # cv2.waitKey(1)
            height, width, bytesPerComponent = resized_image.shape
            # print(height, width)
            bytesPerLine = 3 * width
            # print(bytesPerLine)
            cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB, resized_image)
            # print("pass cvtColor")

            q_image = QtGui.QImage(resized_image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
            # print("pass QImage")

            pixmap = QtGui.QPixmap.fromImage(q_image)
            # print("pass pixmap")
            self.image_editor.setPixmap(pixmap)
            # self.image_disp.setScaledContents(True)
            # print("pass set pixel map")

            self.image_editor = image_painter(self.image_disp)
            self.image_editor.setCursor(QtCore.Qt.CrossCursor)

            reload_menu.cancel()
            # threading.join()

            # print("pass set cursor")

            # self.image_editor.update()
            # self.show()

    # def select_reference_image(self):
    #     window.setCurrentWidget(window_image_browser)


class image_painter(QLabel):
    origin_x = 0
    origin_y = 0
    width = 0
    height = 0
    flag = False

    def mousePressEvent(self, event):
        self.flag = True
        self.origin_x = event.x()
        self.origin_y = event.y()

    def mouseReleaseEvent(self, event):
        self.flag = False

    def mouseMoveEvent(self, event):
        if self.flag:
            self.width = event.x()
            self.height = event.y()
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        rectangle = QtCore.QRect(self.origin_x, self.origin_y, abs(self.width - self.origin_x), abs(self.height - self.origin_y))
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine))
        painter.drawRect(rectangle)

app = QApplication(sys.argv)

window = QtWidgets.QStackedWidget()

window_define_parking_lot = define_parking_lot()

window.addWidget(window_define_parking_lot)

window.setWindowTitle("Image Calibration")

window.setFixedWidth(1280)
window.setFixedHeight(720)
window.show()

app.exec_()