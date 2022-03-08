from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog, QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QPixmap
import sys
import os
import cv2
import threading


parent = os.getcwd()

reference_filename = ""
previous_reference_filename = ""
global window_define_parking_lot

class image_browser(QMainWindow):
    global reference_filename

    def __init__(self):
        super(image_browser, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('select-reference-image.ui', self) # Load the .ui file

        self.next_B.clicked.connect(self.define_park_lot)
        self.browse_B.clicked.connect(self.browse_image)
        self.reset_image_B.clicked.connect(self.reset_image)
        self.cam_image_B.clicked.connect(self.camera_capture)

        self.show() # Show the GUI

    def define_park_lot(self):
        # print(reference_filename)
        window.setCurrentWidget(window_define_parking_lot)

    def browse_image(self):
        global reference_filename
        # print("Browsing for reference image")
        filename = QFileDialog.getOpenFileName(self, 'Select File', parent, 'Images (*.png;*.jpg;*.jpeg)')
        self.image_name.setText(filename[0])
        # print(filename)
        # print(filename[0])
        reference_filename = filename[0]
        pixmap = QPixmap(filename[0])
        self.image_disp.setPixmap(pixmap)
        self.image_disp.setScaledContents(True)

    def reset_image(self):
        global reference_filename
        print("Reset image content")
        pixmap = QPixmap(None)
        self.image_name.setText("")
        reference_filename = ""
        self.image_disp.setPixmap(pixmap)

    def camera_capture(self):
        global reference_filename
        print("Capture from Camera")
        # Import additional function to access the camera
        # Fix after retrieve the camera for an another test
        reference_filename = 'images\camera-capture-dummy.jpg'
        pixmap = QPixmap(reference_filename)
        self.image_disp.setPixmap(pixmap)
        self.image_disp.setScaledContents(True)
        self.image_name.setText("Capture from Camera")

class define_parking_lot(QMainWindow):
    global reference_filename
    global previous_reference_filename

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
        self.image_editor.setGeometry(QtCore.QRect(0, 0, 960, 540))

        self.back_B.clicked.connect(self.select_reference_image)
        self.setup_image()

        self.show() # Show the GUI

    def setup_image(self):
        global previous_reference_filename
        global reference_filename
        # self.image_editor = image_painter(self.image_disp)
        print("Define parking lot: {}".format(reference_filename))

        reload_menu = threading.Timer(1.0, self.setup_image)
        reload_menu.start()

        # if reference_filename == "":
        #     pass
        # else:

        if reference_filename == "" and reference_filename == previous_reference_filename:
            print("pass")
            pass
        elif reference_filename == "" and reference_filename != previous_reference_filename:
            print("Reference Image cleared")
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
            print(height, width)
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

            # reload_menu.cancel()

            previous_reference_filename = reference_filename

            # print("pass set cursor")

            self.image_editor.update()
            # self.show()
            #reload_menu.cancel()

    def select_reference_image(self):
        window.setCurrentWidget(window_image_browser)


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
        if (self.width - self.origin_x <= 15) and (self.height - self.origin_y <= 15):
            rectangle = QtCore.QRect(0, 0, 0, 0)
            painter = QtGui.QPainter(self)
            painter.setPen(QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine))
            painter.drawRect(rectangle)
        else:
            rectangle = QtCore.QRect(self.origin_x, self.origin_y, self.width - self.origin_x, self.height - self.origin_y)
            painter = QtGui.QPainter(self)
            painter.setPen(QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine))
            painter.drawRect(rectangle)

app = QApplication(sys.argv)

window = QtWidgets.QStackedWidget()

window_image_browser = image_browser()
window_define_parking_lot = define_parking_lot()

window.addWidget(window_image_browser)

window.addWidget(window_define_parking_lot)

window.setWindowTitle("Image Calibration")

window.setFixedWidth(1280)
window.setFixedHeight(720)
window.show()

app.exec_()